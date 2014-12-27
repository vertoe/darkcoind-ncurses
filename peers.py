#!/usr/bin/env python
import curses, time

import global_mod as g
import footer

def draw_window(state, window):
    window.clear()
    window.refresh()

    win_header = curses.newwin(3, 75, 0, 0)

    if 'peerinfo' in state:
        win_header.addstr(0, 1, "connected peers: " + str(len(state['peerinfo'])).ljust(10) + "                 (UP/DOWN: scroll, P: refresh)", curses.A_BOLD)
        win_header.addstr(2, 1, "  Node IP           Version           Recv      Sent         Time   High", curses.A_BOLD + curses.color_pair(5))
        draw_peers(state)

    else:
        win_header.addstr(0, 1, "no peer information loaded", curses.A_BOLD + curses.color_pair(3))
        win_header.addstr(1, 1, "press 'P' to refresh", curses.A_BOLD)

    win_header.refresh()
    footer.draw_window(state)

def draw_peers(state):
    window_height = state['y'] - 4
    win_peers = curses.newwin(window_height, 75, 3, 0)

    offset = state['peerinfo_offset']

    for index in xrange(offset, offset+window_height):
        if index < len(state['peerinfo']):
            peer = state['peerinfo'][index]

            condition = (index == offset+window_height-1) and (index+1 < len(state['peerinfo']))
            condition = condition or ( (index == offset) and (index > 0) )

            if condition:
                # scrolling up or down is possible
                win_peers.addstr(index-offset, 3, "...")

            else:
                if peer['inbound']:
                    win_peers.addstr(index-offset, 1, 'I')

                elif 'syncnode' in peer:
                    if peer['syncnode']:
                        # syncnodes are outgoing only
                        win_peers.addstr(index-offset, 1, 'S')

                addr_str = peer['addr'].strip("[").strip("]").replace(".onion","").replace(":9999","").replace(":19999","")

                # truncate long ip addresses (ipv6)
                addr_str = (addr_str[:14] + '...') if len(addr_str) > 17 else addr_str

                win_peers.addstr(index-offset, 3, addr_str)
                win_peers.addstr(index-offset, 21, peer['subver'].strip("/").replace("Satoshi:","Sat ").replace("Duffield:","Duf ").replace("Core:","Cor ")[:14])

                mbrecv = "% 7.1f" % ( float(peer['bytesrecv']) / 1048576 )
                mbsent = "% 7.1f" % ( float(peer['bytessent']) / 1048576 )

                win_peers.addstr(index-offset, 35, mbrecv + 'MB')
                win_peers.addstr(index-offset, 45, mbsent + 'MB')

                timedelta = int(time.time() - peer['conntime'])
                m, s = divmod(timedelta, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)

                time_string = ""
                if d:
                    time_string += ("%d" % d + "d").rjust(3) + " "
                    time_string += "%02d" % h + ":"
                elif h:
                    time_string += "%02d" % h + ":"
                time_string += "%02d" % m + ":"
                time_string += "%02d" % s

                win_peers.addstr(index-offset, 55, time_string.rjust(12))

                if 'startingheight' in peer:
                    win_peers.addstr(index-offset, 69, str(peer['startingheight']).rjust(6))

    win_peers.refresh()
