

import os



def enableStartOnBoot(path):
    if not os.path.exists('/home/pi/.config/autostart'):
        os.mkdir('/home/pi/.config/autostart')
    with open('/home/pi/.config/autostart/Start.desktop', 'w') as f:
        f.writelines(['[Desktop Entry]\n',
                    'Name=HBL\n',
                    'Type=Application\n',
                    f'Exec=sh -c "cd {path} && sudo sh start.sh"\n'])
                    
        
def disableStartOnBoot(path):
    with open('/home/pi/.config/autostart/Start.desktop', 'w') as f:
        pass

def isStartOnBootEnabled(path):
    ret = False
    try:
        if os.path.exists('/home/pi/.config/autostart/Start.desktop'):
            with open('/home/pi/.config/autostart/Start.desktop', 'r') as f:

                lines = f.readlines()
                expected = ['[Desktop Entry]',
                        'Name=HBL',
                        'Type=Application',
                        f'Exec=sudo sh {path}/start.sh']
                for line in lines:
                    if path in line:
                        ret = True
                        break
    except Exception as e:
        print(e.__str__())

    return ret

def enableKioscMode(url):
    if not os.path.exists('/home/pi/.config/autostart'):
        os.mkdir('/home/pi/.config/autostart')
    with open('/home/pi/.config/lxsession/LXDE-pi/autostart', 'w') as f:
        f.writelines(['@lxpanel --profile LXDE-pi\n',
                    '@pcmanfm --desktop --profile LXDE-pi\n',
                    'point-rpi\n',
                    f'@chromium --kiosk --noerrdialogs --disable-infobars --no-first-run --ozone-platform=wayland --enable-features=OverlayScrollbar --start-maximized {url}\n'])

def disableKioscMode():
    with open('/home/pi/.config/lxsession/LXDE-pi/autostart', 'w') as f:
        f.writelines(['@lxpanel --profile LXDE-pi\n',
                    '@pcmanfm --desktop --profile LXDE-pi\n',
                    'point-rpi\n'])


def isKioscModeEnabled():
    ret = False
    
    if os.path.exists('/home/pi/.config/lxsession/LXDE-pi/autostart'):
        with open('/home/pi/.config/lxsession/LXDE-pi/autostart', 'r') as f:

                lines = f.readlines()
                
                for line in lines:
                    if 'chromium' in line:
                        ret = True
                        break


    return ret

#/home/pi/.config/lxsession/LXDE-pi
#@lxpanel --profile LXDE-pi
#@pcmanfm --desktop --profile LXDE-pi
##@xscreensaver -no-splash
#point-rpi
#@chromium --kiosk --noerrdialogs --disable-infobars --no-first-run --ozone-platform=wayland --enable-features=OverlayScrollbar --start-maximized http://mercadolibre.com
#