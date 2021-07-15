#! /usr/bin/bash
sudo yum git -y
git clone https://github.com/fafafwzn/the-sentinel.git
cd the-sentinel/cloud-computing
pip3 install gdown
pip3 install -r requirements.txt
gdown https://drive.google.com/uc?id=1QYh8lid_u052BKXMxKiHrX1TVvsEso11