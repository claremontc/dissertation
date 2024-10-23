# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install system-level dependencies required by TensorFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT=8080

# Run the application
CMD ["python", "federatedlearningservice.py"]  