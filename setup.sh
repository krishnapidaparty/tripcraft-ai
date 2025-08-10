#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please add your OpenAI API key to the .env file"
fi

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000
