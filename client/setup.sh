#!/bin/sh

mkdir ./logs
cp ./selog.service /lib/systemd/system/
systemctl enable selog
systemctl status selog
