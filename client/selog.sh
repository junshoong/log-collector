#!/bin/sh

DOWNLOAD_URL="http://log.harveyk.me/download?f="

curl "${DOWNLOAD_URL}selog-client.py" -o /usr/local/bin/selog-client.py
curl "${DOWNLOAD_URL}selog.service" -o /lib/systemd/system/selog.service

yum install -y python-requests
mkdir /var/log/selog
systemctl enable selog
systemctl status selog

