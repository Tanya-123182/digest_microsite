#!/bin/bash
# Setup script for Netlify deployment

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data
mkdir -p static

# Set permissions
chmod +x setup.sh
