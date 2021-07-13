# -*- coding: utf-8 -*-

def test_main_function():
    from app import log, CURRENT_DIR
    
    from app.register import Register as __
    from app.signal_bus import signal_bus, event 

    from app.main import main_function    
    # signal_bus.unsubscribe(event.activate_app)

    from time import sleep
    import threading

    tested_thread = threading.Thread(target=main_function, args=("test_config",))
    tested_thread.start()

    sleep(1)

    assert tested_thread.is_alive()
    assert __.State
    assert __.Config
    assert __.SignalBus
    assert __.Application
    assert __.Builder
    assert __.LayoutEvents
    assert __.MainWindow
    assert __.WelcomeSign
    assert __.WelcomeSign.get_text() == "I am Kr15 GTK App"

    __.SignalBus.emit('quit')
    __.Application.handle_quit('action', 'param')
    tested_thread.join(1)
    del tested_thread
