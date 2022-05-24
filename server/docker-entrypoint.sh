# migrate
echo "Migrating database...";
python3 manage.py migrate;

# collect static files
echo "Collecting static files...";
python3 manage.py collectstatic --noinput;

# run server
echo "Running server...";
gunicorn core.wsgi -b 0.0.0.0:8000;
