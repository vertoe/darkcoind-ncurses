#!/usr/bin/env python
import curses, time

import global_mod as g
import footer

def draw_window(state, window):
    window.clear()
    window.refresh()

    win_header = curses.newwin(3, 75, 0, 0)

    if 'masternodes' in state:
        win_header.addstr(0, 1, "masternode information successfully loaded", curses.A_BOLD + curses.color_pair(2))

    else:
        win_header.addstr(0, 1, "under construction", curses.A_BOLD + curses.color_pair(3))

    win_header.refresh()
    footer.draw_window(state)
