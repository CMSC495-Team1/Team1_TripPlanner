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

# Activate the virtual environment
source "$venv_name/bin/activate"

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Virtual environment '$venv_name' created and activated."
