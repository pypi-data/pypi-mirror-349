# tests/conftest.py

"""
Test configuration and fixtures for ChatMS plugin tests.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure asyncio for tests
def pytest_configure(config):
    """Configure pytest settings."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as an asyncio test"
    )

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        # On Windows with Python 3.8+, use WindowsProactorEventLoop
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Suppress deprecation warnings from pydantic v1/v2 compatibility
@pytest.fixture(autouse=True)
def suppress_warnings():
    """Suppress deprecation warnings during tests."""
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
    warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")