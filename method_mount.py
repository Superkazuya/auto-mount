import os, subprocess

def remove_mount_point_directory(self):
    if not os.access(self.mount_point, os.F_OK):
        return True
    if not os.listdir(self.mount_point):
        #it's a empty directory now (we are running as root so access is not a problem), safe to remove
        os.rmdir(self.mount_point)
        return True
    return False
    #mount point not empty

def create_mount_point_directory(self):
    """FIXME! briefly describe function

    :returns: returns False when there's non-empty directory with the same name
    :rtype: 

    """
    if os.access(self.mount_point, os.F_OK):
        if os.listdir(self.mount_point):
            print("error creating mount point: non-empty directory exists")
            return False
    else:
        os.mkdir(self.mount_point)

    return True
            
def mount_point_chmod(self):
    # if os.access(self.mount_point, os.F_OK):
    #     os.chmod(self.mount_point, 0o755)
    os.chmod(self.mount_point, 0o755)
    

def mount(self):
    """mount this

    :returns: True when success
    :rtype: bool

    """
    while not create_mount_point_directory(self):
        self.__dealwith_name_conflicts()

    mount_point_chmod(self)
    subprocess.check_call(['mount',self.dev['DEVNAME'],self.mount_point])
    print('trying to mount {0}'.format(self))

    return True

def umount(self):
    """PLACE HOLDER

    :returns: True when success, or the device is already unmounted
    :rtype: 

    """
    subprocess.check_call(['umount', '-l', self.mount_point])
    print('trying to unmount {0}'.format(self))
    return remove_mount_point_directory(self)
