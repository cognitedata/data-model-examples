#/bin/bash
if [ $# -eq 0 ]; then
    echo "No arguments supplied"
    exit 1
fi
if [ ! -d ./examples/$1 ]; then
    echo "$1 does not exist as an example!"
fi
echo "Dropping all the data for $1..."
./delete_data.py $1
echo "Load data for $1..."
./load_data.py $1
echo "Run the tranformations for $1..."
./run_transformations.py $1