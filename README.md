# LED wheel

See http://bertspaan.nl/led-wheel.

https://www.raspberrypi.org/downloads/raspbian/

https://computers.tutsplus.com/articles/how-to-clone-raspberry-pi-sd-cards-using-the-command-line-in-os-x--mac-59911

diskutil list
diskutil unmountDisk /dev/disk2
sudo newfs_msdos -F 16 /dev/disk2
sudo dd if=/Users/bert/Downloads/2018-03-13-raspbian-stretch.img of=/dev/rdisk2

https://etcher.io/



https://raspberrypi.stackexchange.com/questions/10251/prepare-sd-card-for-wifi-on-headless-pi

cd /Volumes/boot



```
cd /Volumes/boot
nano wpa_supplicant.conf
```

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=NL

network={
    ssid="StudioPARA"
    psk="zegikniet"
    key_mgmt=WPA-PSK
}
```


LF


https://www.raspberrypi.org/documentation/remote-access/ssh/

```
cd /Volumes/boot
touch ssh
```




https://github.com/adafruit/Adafruit-Pi-Finder/releases/tag/3.0.0



Run `sudo raspi-config`
Enable SPI
I2C
Set locale
Set hostname to `rotor`



- Add user `rotor`: https://www.raspberrypi.org/documentation/linux/usage/users.md
  - `sudo adduser rotor`
  - `sudo usermod -a -G sudo,audio,video,users,netdev,input,spi,i2c,gpio,bluetooth rotor`




ssh rotor@rotor.local










Bluetooth


https://www.cnet.com/how-to/how-to-setup-bluetooth-on-a-raspberry-pi-3/


connect A0:E6:F8:FF:AA:35





## MIDI


sudo apt install libsdl1.2-dev

<!-- sudo apt-get install alsa-utils -->
<!-- sudo apt-get install libasound2-dev -->

<!-- sudo modprobe snd_bcm2835 -->

sudo apt-get install python-pygame
<!-- pip install pygame -->







sudo apt-get install python-smbus




Raspberry Pi 3

- Bedenken welke en hoe dan LED-controller?
- Hoe meten we de rotatiesnelheid?
  - http://www.utopiamechanicus.com/article/arduino-photo-interruptor-slotted-optical-switch/
- Hoe doen we draadloze besturing?
  - https://www.gear4music.com/Keyboards-and-Pianos/Korg-nano-KONTROL-Studio-MIDI-Controller/1GBE
  - https://www.bax-shop.nl/midi-studio-controllers/akai-lpd8-wireless-usb-midi-controller
