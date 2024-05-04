#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3
fi

# Install socket package using pip
echo "Installing socket package..."
pip install socket
