import pyudev, os
from check_mtab import get_mtab_entries
import method_mount 

GLOBAL_MOUNT_PATH = '/media/'

class mountable_device():
    def __init__(self, device_instance):
        self.dev = device_instance
        self.label = self.get_label()
        self.uuid = self.get_uuid()
        self.fstype = self.get_fstype()
        self.mount_point = GLOBAL_MOUNT_PATH

    def __get_attr(self, attr):
        if attr in self.dev:
            return self.dev[attr]
        return None
    
    def get_label(self):
        return self.__get_attr('ID_FS_LABEL')

    def get_uuid(self):
        return self.__get_attr('ID_FS_UUID')

    def get_fstype(self):
        return self.__get_attr('ID_FS_TYPE')

    def get_mount_point(self):
        if self.label:
            self.mount_point += self.label
        elif self.uuid:
            self.mount_point += self.uuid
        elif self.__get_attr('ID_SERIAL'):
            self.mount_point += self.dev['ID_SERIAL']
        else:
            raise NameError('No valid name')
        self.mount_point.replace(' ', r'\040')
        self.__dealwith_name_conflicts()


    # put these methods in a different file
    mount = method_mount.mount
    umount = method_mount.umount


    def __dealwith_name_conflicts(self):
        """when a directory with the same name exists, check if they are the same filesystem. 

        case a: The old filesystem is mounted, and they are identical. => unmount
        case b: The old filesystem is mounted, not identical. => rename, new mount point
        case c: The old filesystem is not mounted. The directory is empty => ignore
        case d: The old filesystem is not mounted. The directory is not empty=> rename, new mount point


        :side_effect: change self.mount_point when needed.
        :returns: 
        :rtype: 

        """
        #conflict
        mtab = get_mtab_entries()
        while os.access(self.mount_point, os.F_OK) and (self.mount_point in mtab or os.listdir(self.mount_point)):
            #while directory exists, and it's mounted or non-empty
            if self.mount_point in mtab:
                #case a,b 
                if self.__need_to_unmount(mtab):
                    #case a
                    #since they use the same mount point, chmod 
                    self.umount()
                else:
                    self.mount_point += '_'
            else:
                #case d
                self.mount_point += '_'
                    
                
        print('{0} is available'.format(self.mount_point))
        
    def __need_to_unmount(self, mtab):
        """check if the occupied mount point belongs to a device file that no longer exists, which means we need to unmount first

        :returns: True if need to unmount
        :rtype: 

        """
        if not os.access(mtab[self.mount_point], os.F_OK):
            return True
        return False
        
    def __repr__(self):
        return (self.mount_point+', '+ self.dev['ID_FS_TYPE'])

    def __str(self):
        return __repr__(self)
        

