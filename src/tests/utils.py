import contextlib

from mock import MagicMock


@contextlib.contextmanager
def mock_signal_receiver(signal, **kwargs):
    """
        Temporarily attaches a receiver to the provided ``signal``
        within the scope of the context manager.
    """
    receiver = MagicMock()
    receiver.__name__ = "mocked_receiver"

    signal.connect(receiver, **kwargs)
    yield receiver
    signal.disconnect(receiver)
