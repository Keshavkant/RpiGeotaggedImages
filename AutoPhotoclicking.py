import subprocess, time, sys, os
from gpiozero import Button

#----------------------------------------------------------------------------#
## VARIABLES ##
SLEEPTIME = 500
BUTTON_GPIO_PIN = 23
SHUTTER_SPEED = 2000 # (IN MICROSECONDS), divide by 1000000 to get shutter speed
#----------------------------------------------------------------------------#

button = Button(BUTTON_GPIO_PIN)
path = r"/home/pi/Desktop/Geotagged_data_captured"
list_subfolders_with_paths = [f.name for f in os.scandir(path) if f.is_dir()]
curr = 1
for folder in list_subfolders_with_paths:
	if folder.startswith('test_images'):
		curr = max(curr, int(folder[11::])-int("0") + 1) 
new_folder = '/home/pi/Desktop/Geotagged_data_captured/test_images' + str(curr).zfill(4)
os.mkdir(new_folder)
subp4 = subprocess.Popen("exec raspistill -t 0", shell = True)
button.wait_for_press()
subp4.kill()
subp6 = subprocess.Popen("exec sudo gpsd /dev/serial0 -F /var/run/gpsd.sock", shell = True)
time.sleep(1)
subp7 = subprocess.Popen("exec gpsmon", shell = True)
button.wait_for_press()
subp7.kill()
subp8 = subprocess.Popen("exec sudo killall gpsd", shell = True)
time.sleep(2)
print('################## starting photo #####################')
subp1 = subprocess.Popen("exec python3 gpslogger.py", shell = True)
subp2 = subprocess.Popen("exec raspistill -n -t 0 -ss " + str(SHUTTER_SPEED) + " -tl 1000 -o " + new_folder + "/photoClicks%04d.jpg", shell = True)
time.sleep(1)
button.wait_for_press()
subp1.kill()
subp2.kill()
## -geosync=+13 is in testing phase
subp3 = subprocess.Popen("exec exiftool -overwrite_original -geotag=/home/pi/datalog.nmea -geosync=+13 " + new_folder, shell = True)
print("Geo-Tagging is in process")
time.sleep(1)
print('##### Press for reboot after you see directory scanned message #####')
button.wait_for_press()
subp3.kill()
subp5 = subprocess.Popen("sudo reboot", shell = True)
sys.exit()
