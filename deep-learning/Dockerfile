# Use the Python3.7.2 image
FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make directories for files
RUN mkdir -p files/recordings
RUN mkdir -p files/generated-frames
RUN mkdir -p files/predicted-frames
RUN mkdir -p files/positive-matches
RUN mkdir -p files/false-positives