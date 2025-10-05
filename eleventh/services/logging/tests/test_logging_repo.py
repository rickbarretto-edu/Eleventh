from eleventh.services.logging.repo import InMemoryLogs


async def test_log_and_all():
    logs = InMemoryLogs()

    await logs.log("first")
    await logs.log("second")
    all_logs = await logs.all()

    assert all_logs == ["first", "second"]

