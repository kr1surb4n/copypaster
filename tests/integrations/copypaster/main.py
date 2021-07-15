# -*- coding: utf-8 -*-

def test_main_function():
    from app import log, CURRENT_DIR
    
    from app.register import Register as __
    from app.signal_bus import signal_bus, event, subscribe
    

    @subscribe
    def activate_app():
        signal_bus.emit(event.quit)

    from app.main import main_function
    main_function('empty')

    from time import sleep
    sleep(1)

    assert __.State
    assert __.Config
    assert __.SignalBus
    assert __.Application
    assert __.Builder
    assert __.LayoutEvents
    assert __.MainWindow
    assert __.WelcomeSign
    assert __.WelcomeSign.get_text() == "I am Kr15 GTK App"