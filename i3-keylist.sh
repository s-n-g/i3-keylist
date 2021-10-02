#!/bin/bash
function help(){
cat << END
usage: $(basename "$0") [-h] [-g GEOMETRY] [-f FORE] [-b BACK] [-k]

i3 Key List Display Utility

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        read keys from this file instead of the default
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

def keys(filename=None, sort_by_key=False):
    if filename is None:
        filename = path.expanduser('~') + '/.config/i3/config'
    try:
        with open(filename, 'r') as f:
            a=f.readlines()
    except:
        print('Error opening ' + filename)
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

filename=None
sort_by_key=False
if len(sys.argv) == 3:
    filename=sys.argv[1]
    if filename == '':
        filename=None
    sort_by_key=sys.argv[2]
elif len(sys.argv) == 2:
    filename=sys.argv[1]
if filename == '-':
    filename=None

print(keys(filename=filename, sort_by_key=sort_by_key))
END
}

width=800
height=600


FILE='-'
DO_SHELL=''
while [ ! -z "$1" ]
do
    case "$1" in
        -h|--help)
            help
            exit
            ;;
        --shell):
            DO_SHELL=1
            shift
            ;;
        -i|--input-file)
            shift
            FILE="$1"
            shift
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
            KEY='-k'
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

if [ -z "$DO_SHELL" ]
then
    python /tmp/$$.py $FILE $KEY | yad \
        --no-buttons \
        --title "i3 Key List" \
        --height $height \
        --width $width \
        $PAR
else
    python /tmp/$$.py $FILE $KEY
fi
rm /tmp/$$.py 2>/dev/null
