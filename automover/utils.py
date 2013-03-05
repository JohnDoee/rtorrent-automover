import os
import platform
import ctypes

# thanks to http://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python
def get_free_space(folder):
    """Return folder/drive free space (in bytes)"""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        return os.statvfs(folder).f_bfree * os.statvfs(folder).f_frsize

def get_size(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    
    return sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(path) for f in files)