echo "Creating venv..."
cd /var/www/html && python3 -m venv venv 

echo "Installing requirements.txt..."
source /var/www/html/venv/bin/activate && pip install -r requirements.txt



echo "Starting runserver on port 8042"
source venv/bin/activate && cd ft_transcendence && python manage.py runserver 0.0.0.0:8042
tail -f /dev/null