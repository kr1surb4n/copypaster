import os

from click.testing import CliRunner

def test_cli():
    from app import cli

    from app.signal_bus import signal_bus, subscribe, emit, event

    from copy import deepcopy
    old_signals = deepcopy(signal_bus.receivers)



    # we subscribe to the signal bus and trigger the quit.
    @subscribe
    def activate_app():
        emit(event.quit)

    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["--debug"])

    assert result.exit_code == 0

    assert "DEBUG" not in result.output
    assert "WARNING" not in result.output
    assert "CRITICAL" not in result.output

    signal_bus.receivers = old_signals