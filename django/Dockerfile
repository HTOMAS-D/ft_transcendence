FROM python:3.12-rc

WORKDIR /var/www/html

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod 777 *
# COPY entrypoint_django.sh .

# RUN pip install --no-cache-dir --upgrade pip setuptools
# RUN pip install --upgrade numpy


# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8042

# Run the Django development server
# ENTRYPOINT [ "tail", "-f", "/dev/null" ]
ENTRYPOINT [ "bash", "entrypoint_django.sh" ]
# ENTRYPOINT [ "/bin/bash", "-c", "/var/www/html/entrypoint_django.sh" ]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8042"]