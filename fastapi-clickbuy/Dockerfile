FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

RUN apt-get -y update

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./

# Install Python libraries specified in requirements.txt.
RUN pip3 install setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .