#!/bin/bash
# wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz
python3 manage.py migrate
sudo cp hackathon.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo service hackathon restart
