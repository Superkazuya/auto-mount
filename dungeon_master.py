import pyudev
import os, sys, fcntl,subprocess
from gi.repository import Notify
from device import mountable_device
from check_mtab import get_mtab_entries
from notification import show_notification

#TODO SIGTERM handling

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

    LOCK_FILE = '/run/dungeon_master.pid'
    lock_file = open(LOCK_FILE, 'w+')
    try:
        fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print("Another instance of this program is already running. Manually remove {0} to unlock.".format(LOCK_FILE))
        sys.exit(0)

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')

    Notify.init("Dungeon Master")

   #polling 
    for action, device in monitor:
        if(action == 'add' and need_to_mount(device)):
            md = mountable_device(device)
            if md.mount():
                mounted_device_list[md.mount_point] = md
                show_notification(md.mount_point, 'mounted')

        elif action == 'remove':
            md = search_mounted_device_list(device)
            if md and md.umount():
                mounted_device_list.pop(md.mount_point)
                show_notification(md.mount_point, 'removed')

        elif action == 'change' and need_to_mount(device):
            md = search_mounted_device_list(device)
            if md:
                md.umount()
                md.mount()
                show_notification(md.mount_point, 'changed')

    fcntl.lockf(lock_file, fcntl.LOCK_UN)
    lock_file.close()
    os.unlink(LOCK_FILE)
    
