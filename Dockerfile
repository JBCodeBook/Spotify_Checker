FROM linux/arm/v7

# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SQLite system package
FROM keinos/sqlite3

# Copy the entire project to the working directory
COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]