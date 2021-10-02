#!/usr/bin/python
import gi
from os import path
from sys import exit
from argparse import ArgumentParser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def keys(filename=None, sort_by_key=False, return_a_string=False):
    if filename is None:
        filename = path.expanduser('~') + '/.config/i3/config'
    try:
        with open(filename, 'r') as f:
            the_lines=f.readlines()
    except:
        print('Error opening ' + filename)
        exit(1)

    the_keys=list(filter(lambda x: True if x.startswith('bindsym') else False, the_lines))

    for i in range(0, len(the_keys)):
        the_keys[i] = the_keys[i].replace('--release', '').replace('bindsym ','').replace('exec ','').replace('--no-startup-id ','').replace('\n','').replace('"', '').replace("'", "").strip().split(' ', 1)
        #print(the_keys[i])


    mmax = max([len(x[0]) for x in the_keys]) + 4

    for i in range(0, len(the_keys)):
        the_keys[i][0] = the_keys[i][0].ljust(mmax)
        if the_keys[i][1].startswith('i3-nagbar'):
            the_keys[i][1] = 'i3-nagbar'

    if sort_by_key:
        the_keys.sort()
    else:
        the_keys.sort(key=lambda x: x[1])

    if not return_a_string:
        return the_keys

    ret = ''
    for i in range(0, len(the_keys)):
        ret = ret + the_keys[i][0] + the_keys[i][1] + '\n'
    return ret

def print_keys(filename=None, sort_by_key=False):
    for n in keys(filename=filename, sort_by_key=sort_by_key):
        print(*n)


class I3wmKeyList(Gtk.Window):

    width = 800
    height = 600

    def __init__(
        self,
        filename=None,
        foreground=None,
        background=None,
        size=None,
        sort_by_key=False
    ):
        super().__init__(title="i3 Key List")

        self.set_border_width(10)
        self.stick()
        textbuffer = Gtk.TextBuffer()
        the_keys = keys(filename=filename, sort_by_key=sort_by_key)
        l = len(the_keys)

        store = Gtk.ListStore(str, str)
        for n in range(0, len(the_keys)):
            treeiter = store.append(the_keys[n])

        tree = Gtk.TreeView(model=store)
        tree.set_can_focus(False)

        data =(('Key', False), ('Command', True))
        renderer = Gtk.CellRendererText()
        if foreground:
            renderer.set_property("foreground", foreground)
        if background:
            renderer.set_property("background", background)
        if size:
            try:
                renderer.set_property("size-points", int(size))
            except ValueError:
                pass
        for i, n in enumerate(data):
            column = Gtk.TreeViewColumn(n[0], renderer, text=i)
            column.set_resizable(True)
            column.set_clickable(True)
            if i == 0:
                column.set_min_width(150)
            column.set_sort_column_id(i)
            column.set_spacing(5)
            column.set_sort_indicator(n[1])
            tree.append_column(column)
            if n[1]:
                column.set_sort_order(Gtk.SortType.ASCENDING)

        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)
        key, modifier = Gtk.accelerator_parse('Escape')
        accel_group.connect(key, modifier, Gtk.AccelFlags.VISIBLE, self.on_close)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(tree)
        self.add(scrolled_window)
        self.set_default_size(self.width, self.height)



    def set_user_geometry(self, geometry):
        w, h = geometry.split('x')
        try:
            self.width = int(w)
            self.height = int(h)
            self.set_default_size(self.width, self.height)
        except ValueError:
            pass

    def on_close(self, *data):
        Gtk.main_quit()

def main():
    parser = ArgumentParser(description='i3 Key List Display Utility')

    parser.add_argument('-i', '--input-file', default=None,
                        help='read keys from this file instead of the default')
    parser.add_argument('-g', '--geometry', default='',
                        help='use this window size (default is 800x600)')
    parser.add_argument('-f', '--fore', default=None,
                        help='set the foreground color')
    parser.add_argument('-b', '--back', default='',
                        help='set the background color')
    parser.add_argument('-s', '--size', default=0,
                        help='set text size')
    parser.add_argument('-k', '--key', default=False, action='store_true',
                        help='sort by key (default is by command)')
    parser.add_argument('--shell', default=False, action='store_true',
                        help='just print the list and exit')

    args = parser.parse_args()

    if args.shell:
        print_keys(filename=args.input_file, sort_by_key=args.key)
        exit()

    window = I3wmKeyList(
        filename=args.input_file,
        foreground=args.fore,
        background=args.back,
        size=args.size,
        sort_by_key=args.key
    )
    window.connect("destroy", Gtk.main_quit)
    if args.geometry:
        window.set_user_geometry(args.geometry)

    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
