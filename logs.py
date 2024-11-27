import logging
from logging.config import dictConfig
from config import log_file


def configure_logging() -> None :
    dictConfig(
        {
            "version" : 1,
            "disable_existing_loggers" : False,
            "filters" : {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
                "correlation_id" : {
                    "()" : "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length" : 8,
                    "default_value" : "-",
                },
            },
            "formatters" : {
                "console" : {
                    "class" : "logging.Formatter",
                    # "datefmt": "%H:%M:%S",
                    # formatter decides how our console logs look, and what info is included.
                    # adding %(correlation_id)s to this format is what make correlation IDs appear in our logs
                    "format" : "%(asctime)s %(levelname)s: [%(correlation_id)s] %(message)s",
                },
                "file" : {
                    "class" : "logging.Formatter",
                    # "datefmt": "%Y-%m-%d %%H:%M:%S",
                    # formatter decides how our console logs look, and what info is included.
                    # adding %(correlation_id)s to this format is what make correlation IDs appear in our logs
                    "format" : "%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s",
                },
            },
            "handlers" : {
                "console" : {
                    "class" : "logging.StreamHandler",
                    # Filter must be declared in the handler, otherwise it won't be included
                    "filters" : ["correlation_id"],
                    "formatter" : "console",
                    # "file": "provisioning.log",
                },
                "file" : {
                    "class" : "logging.FileHandler",
                    # Filter must be declared in the handler, otherwise it won't be included
                    "filters" : ["correlation_id"],
                    "formatter" : "console",
                    "filename" : log_file,
                },
            },
            # Loggers can be specified to set the log-level to log, and which handlers to use
            "loggers" : {
                "asgi_correlation_id" : { "handlers" : ["file"], "level" : "INFO" },
            },
        }
    )

configure_logging()
logger = logging.getLogger("asgi_correlation_id")