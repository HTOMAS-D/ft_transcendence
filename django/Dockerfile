FROM python:3.12-rc

### Volumes:
# There will be a volume mounted to `/code/`
# There might also be a volume mounted to `/logs` for optional logging to files
WORKDIR /code

# Require an appname to run gunicorn
ARG APP_NAME
ENV _APP_NAME=$APP_NAME

# Make sure pip is up to date
RUN pip install --upgrade pip

# Install the requirements required for all the microservices
#
# Although it would be better to only install dependencies required for each
# microservice seperately. This will allow us to have a single docker file for
# each django microservice.
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

# Update PYTHONPATH to also spot a potential share volume
ENV PYTHONPATH "${PYTHONPATH}:/share"

### ENTRYPOINT:
# We will use gunicorn as a webserver. If you want to extra options for a
# certain container you can use the 'GUNICORN_CMD_ARGS' env variable
# Arguments:
# - $_APP_NAME.wsgi  | The wsgi that is run with gunicorn
# - reuse_port       | This gives less errors when quickly rerunning the project
# - reload           | Automatically reloads the server on file changes
# - log-file         | Where to output logs
# - capture_output   | Outputs any STDERR and STDOUT to the logfile
# TODO: SSL certificates

ENTRYPOINT ["sh", "-c", "gunicorn $_APP_NAME.wsgi\
                        --reuse-port\
                        --reload"]

                        # --log-file /logs/gunicorn-error.log\
                        # --capture-output"]
