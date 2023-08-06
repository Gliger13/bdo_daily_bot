"""Tests async event loops creation and management"""
import asyncio
from asyncio import AbstractEventLoop

import pytest


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Rewrite pytest-asyncio event loop to the session scope"""
    default_policy = asyncio.get_event_loop_policy()
    process_event_loop = default_policy.new_event_loop()

    yield process_event_loop

    process_event_loop.close()
