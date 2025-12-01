# Use the official Python image
FROM python:3.13-slim-bookworm

# Set the working directory
WORKDIR /app

# Install dependencies
COPY api/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the files into the container
COPY .env ./.env
COPY api .

# Set the entrypoint to main.py
ENTRYPOINT ["python3", "main.py"]