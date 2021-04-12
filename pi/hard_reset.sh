#! /bin/bash
echo 'Cloning remote files into /home/pi/rawdata/original_files/Hungry-Elephants...'
#First make sure these folders exist
mkdir /home/pi/rawdata/original_files
cd /home/pi/rawdata/original_files
git clone https://github.com/rlsanders4/Hungry-Elephants.git -b release
#Then make sure the branch is up to date
cd /home/pi/rawdata/original_files/Hungry-Elephants
git fetch --all
git reset --hard origin/release

echo 'Resetting all files....'
cp –R /home/pi/rawdata/original_files/Hungry-Elephants/pi /home/pi

echo 'Setting up soft links.....'
rm /home/pi/Desktop/start
ln -s /home/pi/ui.py /home/pi/Desktop/start
rm /home/pi/Desktop/config.ini
ln -s /home/pi/shared_data/config.ini /home/pi/Desktop/config.ini
