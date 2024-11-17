#!/bin/bash

# Check if the virtual environment name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <venv_name>"
    exit 1
fi

venv_name="$1"

# Check if the virtual environment already exists
if [ -d "$venv_name" ]; then
    echo "Virtual environment '$venv_name' already exists."
    exit 1
fi

# Create the virtual environment
python3 -m venv "$venv_name"


# Determine the operating system
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    # Unix-based systems (Linux, macOS)
    source "$venv_name/bin/activate"
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows systems
    source "$venv_name/Scripts/activate"
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Upgrade pip
pip install --upgrade pip

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Virtual environment '$venv_name' created and activated."
