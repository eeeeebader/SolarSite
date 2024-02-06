# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and requirements.txt into the container
COPY ./src /app
COPY ./requirements.txt /app

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Expose the port the application will run on
EXPOSE 8000

# Command to run the Python application
CMD ["python", "app.py"]
