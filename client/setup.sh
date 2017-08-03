#!/bin/sh

yum install -y python-requests
mkdir /var/log/selog
cp ./selog.service /lib/systemd/system/
cp ./selog-client.py /usr/local/bin/selog-client.py
systemctl enable selog
systemctl status selog
