#! /usr/bin/bash
sudo pip3 install virtualenv
virtualenv the-sentinel
source ~/the-sentinel/bin/activate
sudo pip3 install -r requirements.txt --no-cache-dir
gdown https://drive.google.com/uc?id=1QYh8lid_u052BKXMxKiHrX1TVvsEso11