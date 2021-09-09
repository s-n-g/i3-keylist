# i3wm-keylist

Display i3 Window Manager Key List

![2021-09-05-215419_1680x1050_scrot.jpg](2021-09-05-215419_1680x1050_scrot.jpg)

## Table of Contents

<!-- vim-markdown-toc Marked -->

* [Introduction](#introduction)
* [1. Script i3wm-keylist.py](#1.-script-i3wm-keylist.py)
    * [Installation](#installation)
* [2. Script i3wm-keylist.sh](#2.-script-i3wm-keylist.sh)
    * [Installation](#installation)

<!-- vim-markdown-toc -->

## Introduction


This project was inspired by a youtube video by [DistroTube](https://www.youtube.com/channel/UCVls1GmFKf6WlTraIb_IaJg) titled "[Want A List Of Your Keybindings? Write A Shell Script!](https://www.youtube.com/watch?v=WkXyXIs-ZMI)".

The idea is to have a window displaying the key bindings used by i3, much like the window [awsome window manager](https://awesomewm.org/) has.

My first thought was to use BASH shell scripting and see where it get me, but I finally ended up using **python** for it.

So, [PyGObject](https://pygobject.readthedocs.io/) was the way to go: **i3wm-keylist.py** is the product of this effort.

Now, since [GTK](https://www.gtk.org/) is notorious for breaking its theming with each and every release, a shell script (using [YAD](https://github.com/v1cont/yad)) is also availabe: **i3wm-keylist.sh**. This way, it's up to YAD to take care of GTK theme breakages.



## 1. Script i3wm-keylist.py

This is the primary script of this project.

    $ i3wm-keylist.py -h
    usage: i3wm-keylist.py [-h] [-g GEOMETRY] [-f FORE] [-b BACK]
                          [-s SIZE] [-k] [--shell]

    i3wm Key List Display Utility

    optional arguments:
      -h, --help            show this help message and exit
      -g GEOMETRY, --geometry GEOMETRY
                            use this window size (default is 800x600)
      -f FORE, --fore FORE  set the foreground color
      -b BACK, --back BACK  set the background color
      -s SIZE, --size SIZE  set text size
      -k, --key             sort by key (default is by command)
      --shell               just print the list and exit

The sctipt can set the dimension of the window displayed, along with the foreground and background color and size of the text rendered.

### Installation

Just copy the script to any location of your choosing (I will assume that this location is **~/.config/i3/scripts**).

Then, choose a **key binding** to use to execute the script (I will assume **#mod+slash**, i.e. **Super+/**).

Please make sure **PyGObject** is already installed in your system. Package name: **python-gobject** or **python3-gobject** or similar.

    cp i3wm-keylist.py ~/.config/i3/scripts
    echo 'bindsym $mod+slash exec --no-startup-id ~/.config/i3/scripts/i3wm-keylist.py' >> ~/.config/i3/config
    echo 'for_window [title="i3wm Key List"] floating enable border pixel 1' >> ~/.config/i3/config


## 2. Script i3wm-keylist.sh

This is the alternative script of the project.

You should use this script in case the previous one stops working (setting colors and/or text size fails).

Please meke sure [YAD](https://github.com/v1cont/yad) is already installed in your system.

    $ i3wm-keylist.sh -h
    usage: i3wm-keylist.sh [-h] [-g GEOMETRY] [-f FORE] [-b BACK] [-k]

    i3wm Key List Display Utility

    optional arguments:
      -h, --help            show this help message and exit
      -g GEOMETRY, --geometry GEOMETRY
                            use this window size (default is 800x600)
      -f FORE, --fore FORE  set the foreground color
      -b BACK, --back BACK  set the background color
      -k, --key             sort by key (default is by command)

The sctipt can set the dimension of the window displayed, along with the foreground and background color of the text (but not its size).

### Installation

Same thing here. Just copy the script to any location of your choosing (I will again assume that this location is **~/.config/i3/scripts**).

Then, choose a **key binding** to use to execute the script (I will again assume **#mod+slash**, i.e. **Super+/**).

    cp i3wm-keylist.sh ~/.config/i3/scripts
    echo 'bindsym $mod+slash exec --no-startup-id ~/.config/i3/scripts/i3wm-keylist.sh >> ~/.config/i3/config
    echo 'for_window [title="i3wm Key List"] floating enable border pixel 1' >> ~/.config/i3/config




