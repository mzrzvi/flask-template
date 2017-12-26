# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app_name
WORKDIR /app

# Copy the current directory contents into the container at /app_name
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80
EXPOSE 5000

ARG ENVIRONMENT=PRODUCTION
ARG PORT=80

ENV ENVIRONMENT ${ENVIRONMENT}
ENV PORT ${PORT}

ENTRYPOINT ["python"]

CMD ["run.py"]