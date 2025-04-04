# Home Computer Main Module
# Author: Daniel Ervilha
# Type: main
import sys
import time
from datetime import datetime, timedelta

import terminal
from i_app import Page, BaseApp
from interface import MainInterface

FRAME_INTERVAL = 0.02

def run(app: BaseApp):
    # Start main page
    width, height = terminal.size()
    main_page = Page(width, height)

    # Start application
    app.start(main_page)

    t0 = datetime.now()
    delta_time = 0.001
    try:
        while app.is_running():
            _w, _h = terminal.size()
            if _w != width or _h != height: # resize
                width = _w
                height = _h
                main_page = Page(width, height)
                terminal.force_input({'type': terminal.EVENT_RESIZE})

            # Read events from OS specific SDK
            events = []
            while event := terminal.read_input():
                events.append(event)

            # Update app & draw
            app.update(main_page, delta_time, events)
            main_page.draw(0, 0)

            # Frametime sleep
            time.sleep(FRAME_INTERVAL)
            t1 = datetime.now()
            delta_time = float((t1 - t0).microseconds) / 1_000_000
            t0 = t1

    finally:
        app.terminate(main_page)


def entry_standalone():
    terminal.clear_screen()
    terminal.hide_cursor()
    app = MainInterface()
    run(app)


def entry_args(args: list[str]):
    ...


if __name__ == '__main__':
    if len(sys.argv) == 1:
        entry_standalone()
    else:
        entry_args(sys.argv[1:])

    # test: Test = eval("Test()")
    # test.call()
