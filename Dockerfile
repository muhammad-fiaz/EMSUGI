# Use the latest Python runtime as a base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (or any port your app uses)
EXPOSE 8000

# Run the application
CMD ["python", "launch.py"]
