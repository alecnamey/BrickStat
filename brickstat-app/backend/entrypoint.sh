#!/bin/sh
set -e


# Start Gunicorn
printf "Starting Gunicorn...\n"
exec gunicorn -w 4 -b 0.0.0.0:5000 backend:app
