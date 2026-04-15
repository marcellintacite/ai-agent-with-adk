from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import settings
from src.logger import setup_logging, logger

# Constants
DATA_DIR = Path(settings.DATABASE_URL).parent
DB_FILE = Path(settings.DATABASE_URL)
PRODUCTS_FILE = Path(settings.PRODUCTS_FILE)


def normalize_search_text(value: str) -> str:
    # Normalize accents, units, and spacing for robust free-text matching.
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"(\d+)\s*(go|gb)\b", r"\1gb", text)
    text = re.sub(r"(\d+)\s*(to|tb)\b", r"\1tb", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compact_search_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def flatten_specs(value: Any) -> list[str]:
    parts: list[str] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            parts.append(str(key))
            parts.extend(flatten_specs(nested_value))
    elif isinstance(value, list):
        for nested_value in value:
            parts.extend(flatten_specs(nested_value))
    elif value is not None:
        parts.append(str(value))
    return parts


def build_search_blob(item: dict[str, Any]) -> str:
    parts: list[str] = [
        str(item.get("id", "")),
        str(item.get("name", "")),
        str(item.get("description", "")),
        str(item.get("category", "")),
        str(item.get("currency", "")),
        str(item.get("price", "")),
    ]
    parts.extend(flatten_specs(item.get("specs", {})))
    return " ".join(parts)


def matches_query(item: dict[str, Any], query: str) -> bool:
    query_norm = normalize_search_text(query)
    query_terms = [term for term in query_norm.split(" ") if term]
    query_compact = compact_search_text(query_norm)

    blob_norm = normalize_search_text(build_search_blob(item))
    blob_compact = compact_search_text(blob_norm)

    # Any direct compact phrase match is a strong hit (e.g. "512ssd").
    if query_compact and query_compact in blob_compact:
        return True

    # Otherwise require all terms to appear in normalized or compact text.
    return all(term in blob_norm or term in blob_compact for term in query_terms)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_products() -> list[dict[str, Any]]:
    try:
        with PRODUCTS_FILE.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        logger.error("Failed to load products.json", error=str(exc))
        return []


def get_db_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    logger.info("Initializing database...")
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                city TEXT,
                address TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
    logger.info("Database initialized successfully.")


def row_to_customer(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "full_name": row["full_name"],
        "email": row["email"],
        "phone": row["phone"],
        "city": row["city"],
        "address": row["address"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


# Initial data load
PRODUCTS = load_products()
PRODUCT_IDS = {product["id"]: product for product in PRODUCTS}


# Pydantic Schemas
class CustomerCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    city: str | None = Field(default=None, max_length=80)
    address: str | None = Field(default=None, max_length=255)


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    email: str | None = Field(default=None, min_length=5, max_length=255)
    phone: str | None = Field(default=None, max_length=40)
    city: str | None = Field(default=None, max_length=80)
    address: str | None = Field(default=None, max_length=255)


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str
    products: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.LOG_LEVEL)
    init_db()
    logger.info("Service started", app_name=settings.APP_NAME, version=settings.VERSION)
    yield
    logger.info("Service stopping...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Electronics catalog and customer management API.",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> dict[str, Any]:
    return {
        "service": settings.APP_NAME,
        "status": "ok",
        "version": settings.VERSION,
        "products": len(PRODUCTS),
    }


@app.get("/products")
def list_products(
    category: str | None = None,
    available: bool | None = None,
    q: str | None = Query(
        default=None,
        description="Search by name, description, category, and specs (RAM/SSD/CPU/etc.)",
    ),
) -> list[dict[str, Any]]:
    items = PRODUCTS

    if category:
        items = [item for item in items if item["category"].lower() == category.lower()]

    if available is not None:
        items = [item for item in items if item["available"] is available]

    if q:
        items = [item for item in items if matches_query(item, q)]

    return items


@app.get("/products/{product_id}")
def get_product(product_id: str) -> dict[str, Any]:
    product = PRODUCT_IDS.get(product_id)
    if not product:
        logger.warning("Product not found", product_id=product_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.get("/products/categories")
def product_categories() -> dict[str, Any]:
    categories = sorted({item["category"] for item in PRODUCTS})
    return {"count": len(categories), "categories": categories}


@app.get("/customers")
def list_customers() -> list[dict[str, Any]]:
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM customers ORDER BY created_at DESC"
        ).fetchall()
    return [row_to_customer(row) for row in rows]


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int) -> dict[str, Any]:
    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    return row_to_customer(row)


@app.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate) -> dict[str, Any]:
    now = utc_now()
    logger.info("Creating new customer", email=payload.email)

    try:
        with get_db_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO customers (full_name, email, phone, city, address, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.full_name.strip(),
                    payload.email.strip().lower(),
                    payload.phone.strip() if payload.phone else None,
                    payload.city.strip() if payload.city else None,
                    payload.address.strip() if payload.address else None,
                    now,
                    now,
                ),
            )
            connection.commit()
            row = connection.execute(
                "SELECT * FROM customers WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
    except sqlite3.IntegrityError as exc:
        logger.error("Customer creation failed - conflict", email=payload.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A customer with that email already exists",
        ) from exc

    return row_to_customer(row)


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, payload: CustomerUpdate) -> dict[str, Any]:
    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        data = row_to_customer(row)
        updates = payload.model_dump(exclude_unset=True)

        if not updates:
            return data

        # Strip strings if provided
        for field in ["email", "full_name", "phone", "city", "address"]:
            if field in updates and isinstance(updates[field], str):
                updates[field] = updates[field].strip()
                if field == "email":
                    updates[field] = updates[field].lower()

        updates["updated_at"] = utc_now()
        set_clause = ", ".join(f"{field} = ?" for field in updates)
        parameters = list(updates.values()) + [customer_id]

        try:
            connection.execute(
                f"UPDATE customers SET {set_clause} WHERE id = ?",
                parameters,
            )
            connection.commit()
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A customer with that email already exists",
            ) from exc

        updated = connection.execute(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,),
        ).fetchone()

    return row_to_customer(updated)


@app.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int) -> None:
    logger.info("Deleting customer", customer_id=customer_id)
    with get_db_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM customers WHERE id = ?",
            (customer_id,),
        )
        connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
