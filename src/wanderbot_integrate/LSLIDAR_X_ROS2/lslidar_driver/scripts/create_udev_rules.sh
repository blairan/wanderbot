#!/bin/bash
sudo cp lsn10.rules  /etc/udev/rules.d
sudo service udev reload
sudo service udev restart
