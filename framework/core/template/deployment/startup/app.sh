cp /apps/deployment/conf/nginx.conf /etc/nginx/nginx.conf && \
exec gunicorn server:application --config /apps/deployment/conf/gunicorn.py &
exec nginx -g 'pid /tmp/nginx.pid;'