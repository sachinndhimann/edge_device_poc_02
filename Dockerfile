# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the startup script is executable
RUN chmod +x start.sh

# Expose port 5000
EXPOSE 5000

# Run the startup script
CMD ["./start.sh"]
