#!/bin/bash

# Function to print usage instructions
print_usage() {
    echo "Usage: $0"
}

# Function to create and activate a virtual environment
create_venv() {
    local venv_name="venv"

    # Check if the virtual environment already exists
    if [ -d "$venv_name" ]; then
        echo "Virtual environment '$venv_name' already exists."
    else
        # Create the virtual environment
        python3 -m venv "$venv_name"

        # Activate the virtual environment based on the OS
        if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
            source "$venv_name/bin/activate"
        elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source "$venv_name/Scripts/activate"
        else
            echo "Unsupported OS: $OSTYPE"
            return 1
        fi

        # Upgrade pip to the latest version
        pip install --upgrade pip

        # Install requirements from requirements.txt if it exists
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi

        echo "Virtual environment '$venv_name' created and activated."
    fi
}


# Main script execution
# Create and activate the virtual environment
create_venv
