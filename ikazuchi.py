import pyudev
import os
from device import mountable_device
from check_mtab import get_mtab_entries

#TODO make this a singleton
#TODO use mtab and fstab
#TODO use logging or syslog
#TODO what if the system is shut down. probably umount all and delete all directory?
#Need to run as root



context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')

mounted_device_list = {}
#not really a list. Key => mount_point

def search_mounted_device_list(dev):
    for d in mounted_device_list:
        if mounted_device_list[d].dev == dev:
            return mounted_device_list[d]
    return None

def need_to_mount(dev):
    if(dev['DEVTYPE'] == 'partition' or dev['DEVTYPE'] == 'disk'):
        if 'ID_FS_USAGE' in dev:
            return True
    return False


if __name__ == '__main__':
    for action, device in monitor:
        if(action == 'add' and need_to_mount(device)):
            print("new mountable device")
            md = mountable_device(device)
            if md.mount():
                mounted_device_list[md.mount_point] = md
        elif action == 'remove':
            md = search_mounted_device_list(device)
            if md:
                if md.umount():
                    mounted_device_list.pop(mounted_dev.mount_point)

        elif action == 'change' and need_to_mount(device):
            md = search_mounted_device_list(device)
            if not md:
                #not our business
                continue
            md.umount()
            md.mount()
                
            
                    

