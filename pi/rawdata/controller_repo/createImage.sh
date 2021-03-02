#!/bin/bash
CURRENTDATE=$(date '+%Y_%m_%d-%H.%M.%S');
echo 'Creating images'
sudo dd if=/dev/mmcblk0 of=/media/pi/micro/${CURRENTDATE}.img bs=1M count=5000
cd /media/pi/micro
echo 'Shrinking'
sudo pishrink.sh -z ${CURRENTDATE}.img