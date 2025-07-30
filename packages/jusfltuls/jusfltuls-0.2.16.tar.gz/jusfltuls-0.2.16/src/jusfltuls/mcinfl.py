import curses
import click
import logging


import jusfltuls.mcinfl_library as maninf
#from  jusfltuls.mcinfl_library import user_glob # set this for all session
import sys

def get_left_panel_status():
    res = maninf.show_databases()
    logging.debug(f"{res}")
    return res#["file1.txt", "file2.txt", "dir1/", "file3.log"]

def get_right_panel_status():
    res = maninf.show_databases()
    logging.debug(f"{res}")# return ["doc1.pdf", "image.png", "music.mp3", "video.mp4"]
    return res
    #return ["doc1.pdf", "image.png", "music.mp3", "video.mp4"]


def show_message_box(stdscr, message):
    lines = [line.strip() for line in message.strip().split('\n')]
    h, w = stdscr.getmaxyx()
    #
    box_h = 8
    if len(lines) > 6 and len(lines) < h - 3:
        box_h = len(lines) + 2
    elif len(lines) > 6:
        box_h = h - 1
    box_w = max(len(line) for line in lines) + 4
    if box_w > w - 2:
        box_w = w - 2
    #
    win = curses.newwin(box_h, box_w, (h - box_h)//2, (w - box_w)//2)
    win.box()
    for i, line in enumerate(lines[:box_h - 2]):
        win.addstr(1 + i, 2, line[:box_w - 4])
    win.refresh()
    win.getch()  # wait for key press
    win.clear()
    stdscr.refresh()



def confirm_dialog(stdscr, prompt):
    h, w = stdscr.getmaxyx()
    win = curses.newwin(5, len(prompt) + 12, h//2 - 2, (w - len(prompt) - 12)//2)
    win.box()
    win.addstr(1, 2, prompt)
    win.addstr(3, 4, "Yes (y) / No (n)")
    win.refresh()
    while True:
        c = win.getch()
        if c in (ord('y'), ord('Y')):
            return True
        elif c in (ord('n'), ord('N')):
            return False



def on_copy(name, dbase, other_dbase, stdscr, wordcopy="COPY"):
    logging.debug(f"copying - {name}/{dbase} -> {other_dbase};")
    if stdscr:
        confirm = confirm_dialog(stdscr, f"{wordcopy} measurement '{name}' of {dbase} TO {other_dbase}?")
        if confirm:
            if (name is None) or (dbase is None) or (other_dbase is None):
                pass
            else:
                res = maninf.copy_measurement(name, dbase, other_dbase, silent=True)
                logging.debug( f"{res}")
            logging.debug(f"copied '{name}'")
        else:
            logging.debug(f"copying cancelled for '{name}'")
    else:
        # If no stdscr provided, assume yes or handle differently
        # maninf.drop_database(name)
        logging.debug(f"copied '{name}' without confirmation")
    pass

def on_move():
    logging.debug(f"moving - ;")
    pass

def on_create_database(name):
    logging.debug(f"creating new thing - {name};")
    if name is None or len(name) == 0:
        return
    maninf.create_database(name)
    pass

def on_delete_database(name, stdscr):
    logging.debug(f"deleting database - {name};")

    if stdscr:
        confirm = confirm_dialog(stdscr, f"Delete '{name}'?")
        if confirm:
            maninf.drop_database(name)
            logging.debug(f"Deleted '{name}'")
        else:
            logging.debug(f"Deletion cancelled for '{name}'")
    else:
        # If no stdscr provided, assume yes or handle differently
        # maninf.drop_database(name)
        logging.debug(f"Deleted '{name}' without confirmation")


def on_delete_measurement(name, database, stdscr, asking=True):
    """
    I took the same as delete database
    """
    logging.debug(f"deleting measurement - {name} from {database};")

    if stdscr:
        confirm = True
        if asking:
            confirm = confirm_dialog(stdscr, f"Delete '{name}' of {database}?")
        if confirm:
            maninf.delete_measurement(name, database)
            logging.debug(f"Deleted measurement '{name}' from {database}")
        else:
            logging.debug(f"Deletion cancelled for meas. '{name}' of {database}")
    else:
        # If no stdscr provided, assume yes or handle differently
        # maninf.drop_database(name)
        logging.debug(f"Deleted '{name}' without confirmation")


def draw_panel(win, items, selected_idx, active):
    h, w = win.getmaxyx()
    win.clear()
    for idx, item in enumerate(items):
        if idx == selected_idx:
            mode = curses.A_REVERSE if active else curses.A_BOLD
        else:
            mode = curses.A_NORMAL
        if idx < h - 2:
            win.addstr(idx + 1, 1, item[:w-3], mode)
    win.box()
    win.refresh()

def draw_bottom_bar(stdscr):
    h, w = stdscr.getmaxyx()
    bar_text = " 2 Export  3 View  4 Insert  5 Copy  6 Move  7 Create  8 Delete "
    stdscr.attron(curses.A_REVERSE)
    # Truncate bar_text if wider than screen width
    text = bar_text[:w]
    try:
        stdscr.addstr(h-1, 0, text.ljust(w))
    except curses.error:
        # In case window too small, ignore error
        pass
    stdscr.attroff(curses.A_REVERSE)
    stdscr.refresh()

def input_dialog(stdscr, prompt):
    curses.echo()
    h, w = stdscr.getmaxyx()
    win = curses.newwin(3, w//2, h//2 - 1, w//4)
    win.box()
    win.addstr(1, 2, prompt)
    win.refresh()
    stdscr.refresh()
    curses.curs_set(1)
    input_win = curses.newwin(1, w//2 - len(prompt) - 4, h//2, w//4 + len(prompt) + 2)
    curses.echo()
    input_win.clear()
    input_win.refresh()
    s = input_win.getstr().decode('utf-8')
    curses.noecho()
    curses.curs_set(0)
    return s

# ================================================================================
#    MAIN *****************************
# --------------------------------------------------------------------------------

@click.command()
@click.option('--logfile', default='/tmp/mcinflux_debug.log', help='Log file path')
@click.option('--user', "-u", is_flag=True, help='Act as user, use user name and pass')
def main(logfile, user):
    global user_glob

    print("Hey, machine is expected in the format like '127.0.0.1' or 'www.example.com' (where --ssl is selected) ")
    logging.basicConfig(filename=logfile, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Debug log started')

    print(f"i... user is {user}")
    maninf.user_glob = user # set this for all session
    print(f"i... userg is {maninf.user_glob}")
    #
    u, p, d =maninf.get_user_pass()
    if u is None or p is None:
        print("X... user o pass problem")
        sys.exit(1)
    #else:        print(f"/{u}/, /{p}/")

    m =maninf.get_local_machine()
    if m is None:
        print("X... machine name problem")
        sys.exit(1)

    print(f"i... user: {u} on machine: {m} , I am going  there")
    def curses_main(stdscr):
        #print("Ciao")
        logging.debug("Ciao")
        left_db_selected = None
        right_db_selected = None

        left_idx_prev = 0
        right_idx_prev = 0

        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        left_items = get_left_panel_status()
        right_items = get_right_panel_status()
        left_idx, right_idx = 0, 0
        active_panel = 'left'

        h, w = stdscr.getmaxyx()
        mid = w // 2

        left_win = curses.newwin(h-1, mid, 0, 0)
        right_win = curses.newwin(h-1, w - mid, 0, mid)


        def refresh_panels():
            nonlocal left_items, right_items, left_idx, right_idx
            if left_db_selected is None:
                left_items = get_left_panel_status()
            else:
                left_items = ['..'] + maninf.show_measurements(left_db_selected)
            if right_db_selected is None:
                right_items = get_right_panel_status()
            else:
                right_items = ['..'] + maninf.show_measurements(right_db_selected)
            left_idx = min(left_idx, len(left_items) - 1) if left_items else 0
            right_idx = min(right_idx, len(right_items) - 1) if right_items else 0

        refresh_panels()

        draw_panel(left_win, left_items, left_idx, active_panel == 'left')
        draw_panel(right_win, right_items, right_idx, active_panel == 'right')
        draw_bottom_bar(stdscr)

        while True:
            key = stdscr.getch()
            if key == 9:  # TAB
                active_panel = 'right' if active_panel == 'left' else 'left'
                if active_panel == 'left':
                    left_idx = max(0, min(left_idx, len(left_items) - 1))
                else:
                    right_idx = max(0, min(right_idx, len(right_items) - 1))
            elif key == curses.KEY_UP:
                if active_panel == 'left':
                    left_idx = max(0, left_idx - 1)
                else:
                    right_idx = max(0, right_idx - 1)
            elif key == curses.KEY_DOWN:
                if active_panel == 'left':
                    left_idx = min(len(left_items) - 1, left_idx + 1)
                else:
                    right_idx = min(len(right_items) - 1, right_idx + 1)
            # ------------------------------------------------------------
            elif key == ord('2'):# --------------------------------- VIEW MEAS
                name = None
                dbase = None
                if active_panel == 'left':
                    name = left_items[left_idx]
                    dbase = left_db_selected
                    other_dbase = right_db_selected
                else:
                    name = right_items[right_idx]
                    dbase = right_db_selected
                    other_dbase = left_db_selected

                res = maninf.export_measurement(name, dbase, silent=True)
                logging.debug(f"{res}")
                #show_message_box(stdscr, f"{res}")
                refresh_panels()

            elif key == ord('3'):# --------------------------------- VIEW MEAS
                name = None
                dbase = None
                if active_panel == 'left':
                    name = left_items[left_idx]
                    dbase = left_db_selected
                    other_dbase = right_db_selected
                else:
                    name = right_items[right_idx]
                    dbase = right_db_selected
                    other_dbase = left_db_selected

                res = maninf.show_measurement_newest_sample(name, dbase, silent=True)
                logging.debug(f"{res}")
                show_message_box(stdscr, f"{res}")
                refresh_panels()

            elif key == ord('4'):# --------------------------------- INSERT MEAS
                name = None
                dbase = None
                if active_panel == 'left':
                    name = left_items[left_idx]
                    dbase = left_db_selected
                    other_dbase = right_db_selected
                else:
                    name = right_items[right_idx]
                    dbase = right_db_selected
                    other_dbase = left_db_selected

                res = maninf.insert_new_measurement("z_test", dbase, silent=True)
                logging.debug(f"{res}")
                #show_message_box(stdscr, f"{res}")
                refresh_panels()

            elif key == ord('5'):# --------------------------------- COPY MEAS
                name = None
                dbase = None
                if active_panel == 'left':
                    name = left_items[left_idx]
                    dbase = left_db_selected
                    other_dbase = right_db_selected
                else:
                    name = right_items[right_idx]
                    dbase = right_db_selected
                    other_dbase = left_db_selected
                on_copy(name, dbase, other_dbase, stdscr)
                refresh_panels()
            elif key == ord('6'):# --------------------------------- MOVE MEAS
                name = None
                dbase = None
                if active_panel == 'left':
                    name = left_items[left_idx]
                    dbase = left_db_selected
                    other_dbase = right_db_selected
                else:
                    name = right_items[right_idx]
                    dbase = right_db_selected
                    other_dbase = left_db_selected
                on_copy(name, dbase, other_dbase, stdscr, wordcopy="MOVE")
                on_delete_measurement(name, dbase, stdscr, asking=False) # in move
                refresh_panels()
                #on_move()
                #refresh_panels()
            elif key == ord('7'):# --------------------------------- CREATE
                name = input_dialog(stdscr, "Create name: ")
                on_create_database(name)
                refresh_panels()
            elif key == ord('8'): # --------------------------------- DELETE
                logging.debug("8... deleting...")
                if active_panel == 'left':
                    if left_items:
                        #logging.debug("8... deleting...left...")
                        #logging.debug(f"8... deleting...left...{left_idx}")
                        selected_item = left_items[left_idx]
                        #logging.debug(f"8... deleting...selected: {selected_item}")
                        if selected_item != '..': #  view ??? meas?
                            name = left_items[left_idx]
                            on_delete_measurement(name, left_db_selected, stdscr)
                        elif left_db_selected is None: #  view datab ???
                            name = left_items[left_idx]
                            on_delete_database(name, stdscr)

                #----origos
                #    name = left_items[left_idx]
                #else:
                #    name = right_items[right_idx]
                #on_delete_database(name, stdscr)
                refresh_panels()
            elif key == ord('r'): # --------------------------------- refresh
                refresh_panels()

            elif key in (curses.KEY_ENTER, 10, 13):
                if active_panel == 'left':
                    logging.debug(f"Left ENTER db-selected=={left_db_selected}")
                    if left_items:
                        selected_item = left_items[left_idx]
                        logging.debug(f"Left ENTER item-selected=={selected_item}")
                        if selected_item == '..': # going up
                            left_db_selected = None
                            left_items = get_left_panel_status()
                            left_idx = left_idx_prev # not 0
                        elif left_db_selected is None:
                            left_db_selected = selected_item
                            left_idx_prev = left_idx # store  previous index
                            left_items = ['..'] + maninf.show_measurements(left_db_selected)
                            left_idx = 0
                        else:
                            logging.debug(f"enter on measurement: see newest; m1={selected_item} db1={left_db_selected}")
                            res = maninf.show_measurement_newest_oldest(selected_item, left_db_selected, silent=True)

                            logging.debug(f"{res}")
                            show_message_box(stdscr, res)
                            pass
                else:
                    logging.debug(f"Right ENTER db-selected=={right_db_selected}")
                    if right_items:
                        selected_item = right_items[right_idx]
                        if selected_item == '..':
                            right_db_selected = None
                            right_items = get_right_panel_status()
                            right_idx = right_idx_prev # 0
                        elif right_db_selected is None:
                            right_db_selected = selected_item
                            right_idx_prev = right_idx # store
                            right_items = ['..'] + maninf.show_measurements(right_db_selected)
                            right_idx = 0
                        else:
                            logging.debug(f"enter on measurement: see newest; m1={selected_item} db1={right_db_selected}")
                            res = maninf.show_measurement_newest_oldest(selected_item, right_db_selected, silent=True)

                            logging.debug(f"{res}")
                            show_message_box(stdscr, res)
                            pass

            # elif key in (curses.KEY_ENTER, 10, 13):
            #     if active_panel == 'left':
            #         if left_items:
            #             left_db_selected = left_items[left_idx]
            #             left_items = maninf.show_measurements(left_db_selected)
            #             left_idx = 0
            #     else:
            #         if right_items:
            #             right_db_selected = right_items[right_idx]
            #             right_items = maninf.show_measurements(right_db_selected)
            #             right_idx = 0

            elif key in (ord('q'), 27):  # q or ESC to quit
                break

            #refresh_panels()
            draw_panel(left_win, left_items, left_idx, active_panel == 'left')
            draw_panel(right_win, right_items, right_idx, active_panel == 'right')
            draw_bottom_bar(stdscr)

    curses.wrapper(curses_main)

if __name__ == "__main__":
    main()
