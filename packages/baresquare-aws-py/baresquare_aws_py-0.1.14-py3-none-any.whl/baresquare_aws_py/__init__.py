"""Baresquare AWS Python utilities.

This package provides AWS-specific utilities for Baresquare services.
"""

from . import authentication
from . import s3
from . import ssm

from baresquare_core_py.logger import setup_logger

logger = setup_logger()
