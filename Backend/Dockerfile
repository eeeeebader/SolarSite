# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and requirements.txt into the container
COPY ./src /app
COPY ./requirements.txt /app

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Replace src/environments/environment.py with the environment.prod.py 
RUN mv src/environments/environment.prod.py src/environments/environment.py

# edit chrontask file to run every 6 minutes the script src/collector.py
RUN echo "*/6 * * * * root python /app/src/collector.py" >> /etc/crontab

# Expose the port the application will run on
EXPOSE 8000

# Command to run the Python application
CMD ["python", "app.py"]
