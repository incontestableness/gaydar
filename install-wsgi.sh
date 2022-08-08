#!/usr/bin/env bash

set -e

read -p "Press enter if you know what you're doing..."

echo -e "\nInstalling dependencies..."
sudo apt install python3-pip apache2 libapache2-mod-wsgi-py3 -y
sudo pip3 install -r requirements.txt --target /usr/lib/python3/dist-packages --upgrade

echo -e "\nCreating gaydar account..."
sudo addgroup --system gaydar
sudo adduser --system --home /var/lib/gaydar/ --ingroup gaydar gaydar

echo -e "\nCopying in source code..."
# This is where the WSGI application will run from
sudo cp -vr . /var/lib/gaydar/gaydar/

echo -e "\nSetting up static content..."
sudo cp -v html/gaydar.html /var/www/html/
# Make static content owned by www-data
sudo chown -v www-data:www-data /var/www/html/gaydar.html
# Make static content read-only
sudo chmod -v 444 /var/www/html/gaydar.html

echo -e "\nConfiguring WSGI..."
sudo cp -vr WSGI/* /etc/apache2/
sudo a2ensite gaydar.conf
sudo systemctl reload apache2

echo -e "\nAll done."
