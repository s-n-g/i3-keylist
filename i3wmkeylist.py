#!/usr/bin/python
import gi
from os import path
from sys import exit
from argparse import ArgumentParser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def keys(sort_by_key=False):
    try:
        with open(path.expanduser('~') + '/.config/i3/config', 'r') as f:
            a=f.readlines()
    except:
        print('Error opening ~/.config/i3/config')
        exit(1)

    f=list(filter(lambda x: True if x.startswith('bindsym') else False, a))

    for i in range(0, len(f)):
        f[i] = f[i].replace('--release', '').replace('bindsym ','').replace('exec ','').replace('--no-startup-id ','').replace('\n','').replace('"', '').replace("'", "").split(' ', 1)
        #print(f[i])


    mmax = max([len(x[0]) for x in f]) + 4

    for i in range(0, len(f)):
        f[i][0] = f[i][0].ljust(mmax)
        if f[i][1].startswith('i3-nagbar'):
            f[i][1] = 'i3-nagbar'

    if sort_by_key:
        f.sort()
    else:
        f.sort(key=lambda x: x[1])

    ret = ''
    for i in range(0, len(f)):
        ret = ret + f[i][0] + f[i][1] + '\n'
    return ret

def print_keys(sort_by_key=False):
    print(keys(sort_by_key))


class I3wmKeyList(Gtk.Window):

    width = 800
    height = 600
    sort_by_key = False

    def __init__(self):
        super().__init__(title="i3wm Key List")

        self.set_border_width(10)
        self.stick()
        textbuffer = Gtk.TextBuffer()
        s = keys(self.sort_by_key)
        l = len(s)
        textbuffer.set_text(s, l)

        self.text_view = Gtk.TextView.new_with_buffer(textbuffer)
        self.text_view.set_editable(False)
        self.text_view.set_monospace(True)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_name('i3wmkeylist_textview')

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
        css = '#i3wmkeylist_textview text { background-color: ' + back + '; }'
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
    parser = ArgumentParser(description='i3wm Key List Display Utility')

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
        print_keys(args.key)
        exit()

    #if args.back:
    #    css = '#i3wmkeylist_textview text { background-color: ' + args.back + '; }'
    #    css_provider = Gtk.CssProvider()
    #    css_provider.load_from_data(str.encode(css))

    #    Gtk.StyleContext.add_provider_for_screen(
    #        Gdk.Screen.get_default(),
    #        css_provider,
    #        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    window = I3wmKeyList()
    window.connect("destroy", Gtk.main_quit)
    if args.geometry:
        window.set_user_geometry(args.geometry)

    window.set_foreground(args.fore, args.size)

    if args.key:
        window.sort_by_key = True

    if args.back:
        window.set_background(args.back)

    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
