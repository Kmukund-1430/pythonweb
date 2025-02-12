# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Define entrypoint script
ENTRYPOINT ["python"]

# Define CMD to run the application
CMD ["app.py"]
