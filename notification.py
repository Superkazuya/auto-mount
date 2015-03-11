import re, subprocess, os
from gi.repository import Notify

GLOBAL_NOTIFICATION_FORMAT_TITLE = r'<span color="#ef5800"><big><b>Dungeon Master</b></big></span>'
GLOBAL_NOTIFICATION_FORMAT_MESSAGE = r'Device <span color="#afd700">{0}</span> has been {1}.'

def get_environ_file(pattern):
    """get the pid of the first process whose name matches *pattern*. 
    
    if the return code of the 'pgrep' command is 1, no file matches that pattern, probably X server is not started yet.

    :param pattern: process name pattern
    :returns: '/proc/PID_OF_THE_FIRST_PROCESS/environ
    :rtype: string

    """
    li = []
    try:
        li = subprocess.check_output(['pgrep', pattern]).split()
    except subprocess.CalledProcessError as e:
        if e.returncode != 1:
            raise e
        
    for item in li:
        pid = int(item)
        if pid > 0:
            return '/proc/{0}/environ'.format(pid)
    return None

def get_dbus_session_bus_addr(environ_file):
    with open(environ_file) as f:
        li = f.read().split('\0')

    for item in li:
        m = re.match(r'DBUS_SESSION_BUS_ADDRESS=(.*)', item)
        if m:
            return m.group(1)
        
    
def show_notification(device, event):
    """show notification for an event. 

    NOTE: to use libnotify, need to set environment variable DBUS_SESSION_BUS_ADDRESS first.
    You can find this in ~/.dbus/session-bus/

    :param device: device name
    :param event: event name
    :returns: PARENT: child's pid or negative number CHILD: 0
    :rtype: int

    """
    child_pid = os.fork()
    
    if(child_pid != 0):
        return child_pid
    #child
    tmp = get_environ_file('gnome') #??????????????? probably not a good choice?
    if not tmp:
        os._exit(0)
    tmp = get_dbus_session_bus_addr(tmp)
    if tmp:
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = tmp
    else:
        os.exit(0)
    
    os.setgid(100)
    os.setuid(1000)

    print(os.environ['DBUS_SESSION_BUS_ADDRESS'])

    notification=Notify.Notification.new(GLOBAL_NOTIFICATION_FORMAT_TITLE, GLOBAL_NOTIFICATION_FORMAT_MESSAGE.format(device, event), "dialog-information")
    notification.show()
    #print("return value is", subprocess.check_call(['notify-send', GLOBAL_NOTIFICATION_FORMAT_TITLE, GLOBAL_NOTIFICATION_FORMAT_MESSAGE.format(device, event)]))
    os._exit(0)
    #no exception ignored info
    

