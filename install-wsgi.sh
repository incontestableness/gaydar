#!/usr/bin/env bash

set -e

if [[ $UID == 0 ]]; then
	echo "This script should not be run as root!"
	exit 1;
fi

if [[ -z $NOAUTOINSTALL ]]; then
	ASSUMPTION="--assume-yes"
	echo "This script will automatically install packages via apt. --assume-yes is currently enabled!"
	echo "You can disable this behavior by setting the NOAUTOINSTALL environment variable to any value."
else
	ASSUMPTION=""
	echo "Manual prompting by apt is enabled."
fi
read -p "Press enter if you know exactly what you're doing..."; echo

echo -e "Installing Python 3 and pip..."
sudo apt install python3 python3-pip $ASSUMPTION # python3-pip depends on python3 but whatever
echo -e "\nInstalling apache2 and mod_wsgi..."
sudo apt install apache2 libapache2-mod-wsgi-py3 $ASSUMPTION
echo -e "\nInstalling system-wide Python modules..."
sudo pip3 install -r requirements.txt

echo -e "\nCreating gaydar system account..."
sudo addgroup --system gaydar
sudo adduser --system --home /var/lib/gaydar/ --ingroup gaydar gaydar

echo -e "\nInstalling source code..."
# This is where the WSGI application will run from
sudo cp -vr . /var/lib/gaydar/gaydar/

echo -e "\nInstalling static content..."
#sudo cp -v html/gaydar.html /var/www/html/
sudo cp -vR ./html/ /var/www/html/gaydar/
# Make static content owned by www-data
echo -e "\nIs the gaydar dir owned by www-data?"
stat /var/www/html/gaydar/
sudo chown -vR www-data:www-data /var/www/html/gaydar/
# Make static content read-only
# TODO use find maybe
#sudo chmod -v 444 /var/www/html/gaydar.html
sudo chmod -v 555 /var/www/html/gaydar/
sudo chmod -v 444 /var/www/html/gaydar/*

echo -e "\nConfiguring the gaydar apache2 WSGI application..."
sudo cp -vr WSGI/* /etc/apache2/
echo -e "\nEnabling the gaydar WSGI application..."
sudo a2ensite gaydar.conf
echo -e "\nReloading apache2..."
sudo systemctl reload apache2

echo -e "\nAll done."
