@pytest.fixture(scope="session")
def event_loop():
    """
    Overrides the closing behavior of the event loop.

    Overrides the closing behavior of the event loop. Close the event loop only at the end of the session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
