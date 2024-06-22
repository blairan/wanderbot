#!/bin/bash
sudo rm   /etc/udev/rules.d/lsn10.rules
sudo service udev reload
sudo service udev restart
