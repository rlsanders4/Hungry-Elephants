#!/bin/bash
echo -e '\033[0;31mPlease make sure your external drive is mounted! (By double clicking the icon on deaktop or in file manager)\033[0m'
CURRENTDATE=$(date '+%Y_%m_%d-%H.%M.%S');
read -e -p "Enter the external drives' name (after mounting): " FILEPATH
echo Creating images at /media/pi/$FILEPATH
sudo dd if=/dev/mmcblk0 of=/media/pi/$FILEPATH/${CURRENTDATE}.img bs=1M count=5000 status=progress
#sudo pv -tpreb /dev/mmcblk0 | dd of=/media/pi/$FILEPATH/${CURRENTDATE}.img bs=1M count=5000
cd /media/pi/$FILEPATH
echo 'Shrinking'
sudo pishrink.sh -z -a ${CURRENTDATE}.img
echo 'Finished!'
