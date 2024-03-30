# Use the official Python image as the base image
FROM python:3.9

RUN apt-get update && apt-get install -y cron

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and requirements.txt into the container
COPY ./src /app
COPY ./requirements.txt /app

# Install Python packages from requirements.txt
RUN pip install -r requirements.txt

# Replace src/environments/environment.py with the environment.prod.py 
RUN mv environments/environment.prod.py environments/environment.py

COPY cronfile /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Expose the port the application will run on
EXPOSE 8000
# Start the cron service
CMD cron && tail -f /var/log/cron.log & exec python app.py
