#!/bin/sh

mkdir ./logs
cp ./log-col.service /lib/systemd/system/
systemctl enable log-col
systemctl status log-col
