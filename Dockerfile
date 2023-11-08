# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install -r requirements.txt

# Expose the port for your Flask API
EXPOSE 5000

# Start the Flask API
CMD ["python", "app.py"]
