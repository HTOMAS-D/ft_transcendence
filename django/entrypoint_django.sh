echo "Creating venv..."
cd /var/www/html && python3 -m venv venv 

echo "Installing requirements.txt..."
source /var/www/html/env/bin/activate && pip install -r requirements.txt


echo "Starting runserver on port 8042"
python manage.py runserver 0.0.0.0:8042
tail -f /dev/null