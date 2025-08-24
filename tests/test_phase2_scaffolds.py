def test_imports():
    # Import should not raise
    import importlib
    for mod in [
        'src.core.inbox_listener',
        'src.core.command_router',
        'src.core.message_pipeline',
    ]:
        importlib.import_module(mod)


def test_minimal_interfaces():
    from src.core.inbox_listener import InboxListener
    from src.core.command_router import CommandRouter
    from src.core.message_pipeline import MessagePipeline

    listener = InboxListener()
    router = CommandRouter()
    pipeline = MessagePipeline()

    # Minimal methods exist
    assert hasattr(listener, 'start') and hasattr(listener, 'stop')
    assert hasattr(router, 'register') and hasattr(router, 'route')
    assert hasattr(pipeline, 'enqueue') and hasattr(pipeline, 'process_once')


def test_file_tail_and_pipeline(tmp_path):
    from src.core.inbox_listener import InboxListener
    from src.core.message_pipeline import MessagePipeline

    inbox = tmp_path / "inbox"
    inbox.mkdir()
    pipeline = MessagePipeline()
    listener = InboxListener(inbox_dir=str(inbox), pipeline=pipeline, poll_interval_s=0.05)
    try:
        from threading import Event
        event = Event()

        original_enqueue = pipeline.enqueue

        def enqueue_with_event(*args, **kwargs):
            event.set()
            return original_enqueue(*args, **kwargs)

        pipeline.enqueue = enqueue_with_event  # type: ignore[assignment]

        listener.start()
        # Create a message file
        msg = inbox / "001.json"
        msg.write_text('{"from":"Agent-1","to":"Agent-2","message":"hello"}', encoding='utf-8')

        # Wait for listener to enqueue message
        assert event.wait(timeout=1), "Listener did not enqueue message in time"

        item = pipeline.process_once()
        assert item is not None
        to_agent, message = item
        assert to_agent == "Agent-2"
        assert message == "hello"
    finally:
        listener.stop()


def test_default_command_handlers():
    from src.core.command_router import CommandRouter
    router = CommandRouter()
    assert router.route("ping", {"x": 1})["type"] == "pong"
    assert router.route("resume", {"to": "Agent-2"})["action"] == "resume"
    assert router.route("sync", {"to": "Agent-3"})["status"] == "in-sync"


