#!/bin/bash
function help(){
cat << END
usage: $(basename "$0") [-h] [-g GEOMETRY] [-f FORE] [-b BACK] [-k]

i3wm Key List Display Utility

optional arguments:
  -h, --help            show this help message and exit
  -g GEOMETRY, --geometry GEOMETRY
                        use this window size (default is 800x600)
  -f FORE, --fore FORE  set the foreground color
  -b BACK, --back BACK  set the background color
  -k, --key             sort by key (default is by command)

END
}

function create_python(){
cat << END > /tmp/$$.py
from os import path
import sys

def keys(sort_by_key=False):
    try:
        with open(path.expanduser('~') + '/.config/i3/config', 'r') as f:
            a=f.readlines()
    except:
        print('Error opening ~/.config/i3/config')
        sys.exit(1)

    f=list(filter(lambda x: True if x.startswith('bindsym') else False, a))

    for i in range(0, len(f)):
        f[i] = f[i].replace('--release', '').replace('bindsym ','').replace('exec ','').replace('--no-startup-id ','').replace('\n','').replace('"', '').replace("'", "").strip().split(' ', 1)
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

sort_by_key = True if len(sys.argv) > 1 else False
print(keys(sort_by_key))
END
}

width=800
height=600


while [ ! -z "$1" ]
do
    case "$1" in
        -h|--help)
            help
            exit
            ;;
        -g|--geometry)
            shift
            geometry="$1"
            shift

            IFS='x'
            read -ra ADDR <<< "$geometry"
            # for i in "${ADDR[@]}"; do   # access each element of array
            #     echo "$i"
            # done
            IFS=' '
            # echo "length = ${#ADDR[@]}"
            if (( ${#ADDR[@]} == 2 ))
            then
                # make sure both vars are numbers
                x=$((${ADDR[0]} + ${ADDR[1]})) && {
                    width=${ADDR[0]}
                    height=${ADDR[1]}
                }
            fi
            ;;
        -f|--fore)
            shift
            FORE="$1"
            shift
            ;;
        -b|--back)
            shift
            BACK="$1"
            shift
            ;;
        -k|--key)
            KEY=1
            shift
            ;;
        *)
            shift
            ;;
    esac
done

create_python
if [ ! -z "$FORE" ]
then
    PAR="--fore $FORE"
fi
if [ ! -z "$BACK" ]
then
    PAR="$PAR"" ""--back $BACK"
fi
PAR="$PAR"" --text-info"

python /tmp/$$.py | yad \
    --no-buttons \
    --title "i3wm Key List" \
    --height $height \
    --width $width \
    $PAR
rm /tmp/$$.py 2>/dev/null
