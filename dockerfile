<!-- end list -->Dockerfile
# Use an official Python runtime as a parent image
FROM tiangolo/uwsgi-nginx-flask:python3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
