## Bluetooth Serial setup
1. cat /etc/systemd/system/dbus-org.bluez.service
    
    **_Note_**: You should see some text. You should not see file not found.
2. sudo nano /etc/systemd/system/dbus-org.bluez.service
3. Add following line the file
    1. ExecStart=/usr/lib/bluetooth/bluetooth -C
    2. ExecStartPost=/usr/bin/sdptool add SP

4. sudo reboot

## Run Bluetooth Server 

1. Install remote controller android app
    1. Android App:(Arduino & ESP32 Bluetooth Cont)
        https://play.google.com/store/apps/details?id=io.dabbleapp&pcampaignid=web_share
    2. IPhone App: (Dabble - Bluetooth Controller)
        https://apps.apple.com/us/app/dabble-bluetooth-controller/id1472734455 
2. Install python serial lib
    1. pip install pyserial
    2. pip install opencv-python
3. Run Bluetooth server
    1. python bluetoothServer.py