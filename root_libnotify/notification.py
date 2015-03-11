"""This script can be used to send notification to local user desktop as root. 

"""
import re, os
from gi.repository import Notify

GLOBAL_NOTIFICATION_FORMAT_TITLE = r'<span color="#ef5800"><big><b>Dungeon Master</b></big></span>'
GLOBAL_NOTIFICATION_FORMAT_MESSAGE = r'Device <span color="#afd700">{0}</span> has been {1}.'

def get_dbus_session_bus_addr(environ_file):
    with open(environ_file) as f:
        for line in f:
            m = re.match(r'DBUS_SESSION_BUS_ADDRESS=(.*)', line)
            if m:
                return m.group(1)
        
    
def show_notification(notification_title = "", notification_message = "", gid = None, uid = None):
    """show notification for an event. 

    NOTE: to use libnotify, need to set environment variable DBUS_SESSION_BUS_ADDRESS first.
    You can find this in ~/.dbus/session-bus/

    :param notification_title: The title of the notification you want to send
    :param notification_message: The message body of the notification you want to send
    :param gid: group id 
    :param uid: user id
    :returns: PARENT: child's pid or negative number CHILD: 0
    :rtype: int

    """
    child_pid = os.fork()
    if(child_pid != 0):
        return child_pid

    #child
    if gid != None:
        os.setgid(gid)
    if uid != None:
        os.setuid(uid)

    del os.environ['HOME'] 
    #force to use pwd
    file_path = os.path.expanduser(r'~/.dbus/session-bus/')
    tmp = os.listdir(file_path)
    if not tmp:
        os._exit(0)
    tmp = get_dbus_session_bus_addr(file_path+tmp[0])
    if tmp:
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = tmp
    else:
        os.exit(0)

    print(os.environ['DBUS_SESSION_BUS_ADDRESS'])

    #notification=Notify.Notification.new(GLOBAL_NOTIFICATION_FORMAT_TITLE, GLOBAL_NOTIFICATION_FORMAT_MESSAGE.format(device, event), "dialog-information")
    notification=Notify.Notification.new(notification_title, notification_message, "dialog-information")
    try:
        notification.show()
    except:
        pass
    finally:
        os._exit(0)
    #probably X is not started yet. The process' dying anyway. not big deal.

