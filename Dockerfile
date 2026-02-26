FROM node:lts-alpine

# Install system dependencies
RUN apk add --no-cache python3 py3-pip py3-virtualenv bash

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Python virtual environment
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Generate content
RUN . venv/bin/activate && python3 generate.py

# Install frontend tooling
RUN npm install -g bower http-server

# Install bower dependencies
RUN bower install --allow-root

# Expose port
EXPOSE 8080

# Start server
CMD ["http-server", "web", "-p", "8080", "-a", "0.0.0.0"]