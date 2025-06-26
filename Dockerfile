# Use official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy files from your repo into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requiremens.txt

# Run your bot
CMD ["python", "main.py"]
