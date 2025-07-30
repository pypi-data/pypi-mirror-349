"""
Celery app creation
"""

import os
from typing import Any

from celery import Celery
from celery.signals import setup_logging, worker_ready
from loguru import logger
from rich.pretty import pretty_repr

from climate_ref.config import Config
from climate_ref_core.logging import add_log_handler, capture_logging

os.environ.setdefault("CELERY_CONFIG_MODULE", "climate_ref_celery.celeryconf.dev")


def create_celery_app(name: str) -> Celery:
    """
    Create a Celery app

    This function creates a new Celery app with the given name and configuration module.
    The configuration module is loaded from the environment variable `CELERY_CONFIG_MODULE`
    which defaults to `climate_ref_celery.celeryconf.dev` if not set.
    """
    app = Celery(name)
    app.config_from_envvar("CELERY_CONFIG_MODULE")

    return app


@setup_logging.connect
def setup_logging_handler(loglevel: int, **kwargs: Any) -> None:  # pragma: no cover
    """Set up logging for the Celery worker using the celery signal"""
    capture_logging()

    # Include process name in celery logs
    msg_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</green> | <level>{level: <8}</level> | {process.name} | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )

    logger.remove()
    add_log_handler(level=loglevel, format=msg_format, colorize=True)


@worker_ready.connect
def worker_ready_handler(**kwargs: Any) -> None:  # pragma: no cover
    """
    Log a message when the worker is ready
    """
    config = Config.default()
    logger.info(f"Worker ready with config {pretty_repr(config)}")


app = create_celery_app("climate_ref_celery")
