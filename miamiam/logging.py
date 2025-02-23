import structlog

from .settings import Environment, settings

LOG_LEVEL_MAPPER = {
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}


def setup_logging() -> None:
    """
    Configure structured logging for the trading bot application.

    This function sets up structlog with different configurations based on the environment:
    """
    log_level_int = LOG_LEVEL_MAPPER[settings.log_level]
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.dict_tracebacks,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.processors.JSONRenderer()
            if settings.environment == Environment.PRODUCTION
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level_int),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
