import logging
import sys
import structlog


def _resolve_log_level(log_level: str) -> int:
    # Python 3.9-compatible level resolution.
    if isinstance(log_level, str):
        return getattr(logging, log_level.upper(), logging.INFO)
    return int(log_level)


def setup_logging(log_level: str = "INFO"):
    resolved_level = _resolve_log_level(log_level)
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() if str(log_level).upper() != "DEBUG" else structlog.dev.ConsoleRenderer(),
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(resolved_level),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=resolved_level,
    )


logger = structlog.get_logger()
