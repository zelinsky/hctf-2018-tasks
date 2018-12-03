FROM php:7.0-apache-stretch

RUN docker-php-ext-install mysqli pdo pdo_mysql
COPY src/ /var/www/html/
