import logging
import sys
import structlog


def setup_logging(log_level: str = "INFO"):
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() if log_level != "DEBUG" else structlog.dev.ConsoleRenderer(),
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelNamesMapping().get(log_level, logging.INFO)),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )


logger = structlog.get_logger()
