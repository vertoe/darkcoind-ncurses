#!/usr/bin/env python
import curses, time, math
import darkcoin_subsidy as ds

import global_mod as gm
import footer


def draw_window(state, old_window):
    # TODO: only draw parts that actually changed
    old_window.clear()
    old_window.refresh()
    window = curses.newwin(19, 76, 0, 0)

    if 'version' in state:
        if state['testnet'] == 1:
            color = curses.color_pair(2)
            window.addstr(1, 1, "darkcoind v" + state['version'] + " (testnet)", color + curses.A_BOLD)
            unit = 'tDRK'
        else:
            color = curses.color_pair(1)
            window.addstr(1, 1, "darkcoind v" + state['version'] + " ", color + curses.A_BOLD)
            unit = 'DRK'
        window.addstr(0, 1, "darkcoind-ncurses " + gm.version, color + curses.A_BOLD)

    if 'peers' in state:
        if state['peers'] > 0:
            color = 0
        else:
            color = curses.color_pair(3)
        window.addstr(0, 32, str(state['peers']) + " peers    ", color + curses.A_BOLD)

    if 'balance' in state:
        balance_string = "%0.8f" % state['balance'] + " " + unit
        if 'unconfirmedbalance' in state:
            if state['unconfirmedbalance'] != 0:
                balance_string += " (+" + "%0.8f" % state['unconfirmedbalance'] + " unconf)"
        window.addstr(1, 32, balance_string, curses.A_BOLD)

    if 'mininginfo' in state:
        height = str(state['mininginfo']['blocks'])
        if height in state['blocks']:
            blockdata = state['blocks'][str(height)]

            if 'new' in blockdata:
                window.attrset(curses.A_REVERSE + curses.color_pair(5) + curses.A_BOLD)
                blockdata.pop('new')

            window.addstr(3, 1, height.zfill(6) + ": " + str(blockdata['hash']))
            window.addstr(4, 1, str(blockdata['size']) + " bytes (" + str(blockdata['size']/1024) + " KB)       ")
            tx_count = len(blockdata['tx'])
            bytes_per_tx = blockdata['size'] / tx_count
            window.addstr(5, 1, "Transactions: " + str(tx_count) + " (" + str(bytes_per_tx) + " bytes/tx)")

            if 'coinbase_amount' in blockdata:
                bits = int(blockdata['bits'], 16)
                height = blockdata['height']

                if state['testnet'] == 1:
                    block_subsidy = ds.GetBlockBaseValue_testnet(bits, height) / 100000000
                else:
                    block_subsidy = ds.GetBlockBaseValue(bits, height) / 100000000

                if block_subsidy:
                    coinbase_amount = blockdata['coinbase_amount']
                    total_fees = coinbase_amount - block_subsidy # assumption, mostly correct

                    if coinbase_amount > 0:
                        fee_percentage = "%0.2f" % ((total_fees / coinbase_amount) * 100)
                        coinbase_amount_str = "%0.8f" % coinbase_amount
                        window.addstr(7, 1, "Total block reward: " + coinbase_amount_str + " " + unit + " (" + fee_percentage + "% fees)")

                    if tx_count > 1:
                        tx_count -= 1 # the coinbase can't pay a fee
                        fees_per_tx = (total_fees / tx_count) * 1000
                        fees_per_kb = ((total_fees * 1024) / blockdata['size']) * 1000
                        total_fees_str = "%0.8f" % total_fees + " " + unit
                        fees_per_tx = "%0.5f" % fees_per_tx + " m" + unit + "/tx"
                        fees_per_kb = "%0.5f" % fees_per_kb + " m" + unit + "/KB"
                        window.addstr(8, 1, "Fees: " + total_fees_str + " (avg " +  fees_per_tx + ", ~" + fees_per_kb + ")")


            window.addstr(4, 37, "Block timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(blockdata['time'])))

            if state['lastblocktime'] == 0:
                recvdelta_string = "        "
            else:
                recvdelta = int(time.time() - state['lastblocktime'])
                m, s = divmod(recvdelta, 60)
                h, m = divmod(m, 60)
                recvdelta_string = "{:02d}:{:02d}:{:02d}".format(h,m,s)

            stampdelta = int(time.time() - blockdata['time'])
            if stampdelta > 3600*3: # probably syncing if it's three hours old
                stampdelta_string = "             (syncing)"
            elif stampdelta > 0:
                m, s = divmod(stampdelta, 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                stampdelta_string = "({:d}d {:02d}:{:02d}:{:02d} by stamp)".format(d,h,m,s)
            else:
                stampdelta_string = "     (stamp in future)"

            window.addstr(5, 37, "Age: " + recvdelta_string + " " + stampdelta_string)

            if 'chainwork' in blockdata:
                log2_chainwork = math.log(int(blockdata['chainwork'], 16), 2)
                window.addstr(14, 1, "Chain work: 2**" + "%0.6f" % log2_chainwork)

        diff = int(state['mininginfo']['difficulty'])
        window.addstr(10, 1, "Difficulty:  " + "{:,d}".format(diff))

    for block_avg in state['networkhashps']:
        index = 10
        interval = "now"

        if block_avg == 'diff':
            pass
        elif block_avg == 576:
            index += 1
            interval = "24h"
        elif block_avg == 24:
            index += 2
            interval = "1h"
        else:
            break

        rate = state['networkhashps'][block_avg]
        if block_avg != 'diff':
            nextdiff = (rate*150)/(2**32)
            window.addstr(index, 1, "Est. (" + interval.rjust(3) + "): ~" + "{:,d}".format(nextdiff))

        if rate > 10**18:
            rate /= 10**18
            suffix = " EH/s"
        elif rate > 10**12:
            rate /= 10**12
            suffix = " TH/s"
        else:
            rate /= 10**6
            suffix = " MH/s"
        rate_string = "{:,d}".format(rate) + suffix
        window.addstr(index, 37, "Hashrate (" + interval.rjust(3) + "): " + rate_string.rjust(13))
        index += 1

    if 'totalbytesrecv' in state:
        recvmb = "%.2f" % (state['totalbytesrecv']*1.0/1048576)
        sentmb = "%.2f" % (state['totalbytessent']*1.0/1048576)
        recvsent_string = "D/U: " + recvmb + " / " + sentmb + " MB"
        window.addstr(0, 43, recvsent_string.rjust(30), curses.A_BOLD)

    if 'mininginfo' in state:
        pooledtx = state['mininginfo']['pooledtx']
        window.addstr(14, 37, "Mempool transactions: " + "% 5d" % pooledtx)

        errors = state['mininginfo']['errors']
        if len(errors):
            if state['y'] < 20:
                y = state['y'] - 3
            else:
                y = 17
            window.addstr(y, 1, errors[:72], curses.color_pair(5) + curses.A_BOLD + curses.A_REVERSE)
            window.addstr(y+1, 1, errors[72:142].rjust(72), curses.color_pair(5) + curses.A_BOLD + curses.A_REVERSE)

    if 'estimatefee' in state:
        string = "estimatefee:"
        for item in state['estimatefee']:
            if item['value'] > 0:
                string += " (" + str(item['blocks']) + ")" + "%4.2f" % (item['value']*1000) + "m" + unit
        if len(string) > 12:
            window.addstr(15, 37, string)

    window.refresh()
    footer.draw_window(state)
