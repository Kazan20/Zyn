# Use Alpine 3.20.2 as the base image
FROM alpine:3.20.2

# Install necessary packages: Python, pip, ClamAV, and required libraries
RUN apk add --no-cache python3 py3-pip clamav clamav-libunrar

# Install Flask for the web server
RUN apk add py3-flask 

# Update ClamAV database
RUN freshclam

# Set the working directory
WORKDIR /app

# Copy your application files to the container
COPY . /app

# Expose port 8080 for the web server
EXPOSE 8080

# Start the Flask application
CMD ["python3", "/app/app.py"]
