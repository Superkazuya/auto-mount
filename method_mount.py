import os, subprocess
from local_settings import GLOBAL_UID, GLOBAL_GID


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
    os.chown(self.mount_point, GLOBAL_UID, GLOBAL_GID)

def mount(self):
    """mount this

    :returns: True when success
    :rtype: bool

    """
    self.get_mount_point()
    create_mount_point_directory(self)
    #potential race condition?
    MS_FSTYPE = ["msdos", "umsdos", "vfat", "ntfs"]

    if self.fstype in MS_FSTYPE:
        para = ['-o', 'uid={0},gid={1},umask=022,utf8'.format(GLOBAL_UID, GLOBAL_GID)]
        #no space between options!!!
    else:
        para = []

    subprocess.check_call(['mount', self.dev['DEVNAME'],self.mount_point] + para)
    if not self.fstype in MS_FSTYPE:
        mount_point_chmod(self)
    print('{0} mounted'.format(self))

    return True

def umount(self):
    """PLACE HOLDER

    :returns: True when success, or the device is already unmounted
    :rtype: 

    """
    try:
        subprocess.check_call(['umount', '-l', self.mount_point])
    except subprocess.CalledProcessError as e:
        if e.returncode == 32:
            #why would this happen?
            print("Ah oh, an unexpected error occurred!")
        else:
            raise e
            
    print('unmount {0}'.format(self))
    return remove_mount_point_directory(self)
