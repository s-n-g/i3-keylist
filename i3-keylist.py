#!/usr/bin/python
import gi
from os import path
from sys import exit
from argparse import ArgumentParser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def keys(filename=None, sort_by_key=False):
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

    ret = ''
    for i in range(0, len(the_keys)):
        ret = ret + the_keys[i][0] + the_keys[i][1] + '\n'
    return ret

def print_keys(filename=None, sort_by_key=False):
    print(keys(filename=filename, sort_by_key=sort_by_key))


class I3wmKeyList(Gtk.Window):

    width = 800
    height = 600

    def __init__(self, filename=None, sort_by_key=False):
        super().__init__(title="i3 Key List")

        self.set_border_width(10)
        self.stick()
        textbuffer = Gtk.TextBuffer()
        the_keys = keys(filename=filename, sort_by_key=sort_by_key)
        l = len(the_keys)
        textbuffer.set_text(the_keys, l)

        self.text_view = Gtk.TextView.new_with_buffer(textbuffer)
        self.text_view.set_editable(False)
        self.text_view.set_monospace(True)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_name('i3_keylist_textview')

        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)
        key, modifier = Gtk.accelerator_parse('Escape')
        accel_group.connect(key, modifier, Gtk.AccelFlags.VISIBLE, self.on_close)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.text_view)
        self.add(scrolled_window)
        #print('{0}x{1}'.format(self.width, self.height))
        self.set_default_size(self.width, self.height)

    def set_user_geometry(self, geometry):
        w, h = geometry.split('x')
        try:
            self.width = int(w)
            self.height = int(h)
            self.set_default_size(self.width, self.height)
        except ValueError:
            pass

    def set_foreground(self, fore='', size_points=0):
        self._fore = fore
        try:
            self._size_points = int(size_points)
        except:
            self._size_points = 0
        self._apply_tag()

    def set_background(self, back):
        css = '#i3_keylist_textview text { background-color: ' + back + '; }'
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(str.encode(css))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def _apply_tag(self):
        tag = None
        textbuffer = self.text_view.get_buffer()
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        if self._fore and self._size_points > 0:
            tag = textbuffer.create_tag("fore", foreground=self._fore, size_points=self._size_points)
        elif self._size_points > 0:
            tag = textbuffer.create_tag("fore", size_points=self._size_points)
        elif self._fore:
            tag = textbuffer.create_tag("fore", foreground=self._fore)
        if tag:
            textbuffer.apply_tag(tag, start_iter, end_iter)
            self.text_view.set_buffer(textbuffer)


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

    window = I3wmKeyList(filename=args.input_file, sort_by_key=args.key)
    window.connect("destroy", Gtk.main_quit)
    if args.geometry:
        window.set_user_geometry(args.geometry)

    window.set_foreground(args.fore, args.size)

    if args.back:
        window.set_background(args.back)

    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
