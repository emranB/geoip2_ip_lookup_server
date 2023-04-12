#!/bin/sh

# Install required dependencies
pip install -r code/server/requirements.txt

# Get path to current file
get_abs_filename() {
    readlink -m $( dirname -- $0; )
}

# Set root path as environment variable
root=""
if [ "$1" != "" ]
    then
        export root=$1
    else
        export root=$(get_abs_filename)/..
fi

# Save the env var for use by py scripts
export ROOT="$root"

# Set port
port=""
if [ "$2" != "" ]
    then
        port=$2
fi

# Start python app
python "$root/server/app.py" "$port"