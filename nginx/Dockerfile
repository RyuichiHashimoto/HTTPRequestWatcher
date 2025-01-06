FROM nginx:latest

# RUN apt install certbot python3-certbot-nginx -y 

COPY nginx.conf /etc/nginx/nginx.conf
COPY httprequestwatcher.conf /etc/nginx/conf.d/httprequestwatcher.conf

COPY 404.html /var/www/html/404.html