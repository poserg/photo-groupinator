import os
from shutil import copy

def mkdir(path):
    #os.makedirs(path, exist_ok = True)
    try:
      os.makedirs(path)
    except OSError, e:
      #print "Directory is exists"
      pass
    return path
    # d = os.path.dirname(path)
    # if not os.path.exists(d):
    #     os.makedirs(d)
        
    # return d

def get_dir(path, file_name):
  if len(path) > 0 and path[-1] == "/":
    return mkdir(path + file_name)
  else:
    return mkdir(path + "/" + file_name)


def get_dist_path(path, mod_name, file_name):
  return get_dir(path, mod_name) + "/" + os.path.basename(file_name)

def copy_file(image_path, dist_path):
  copy(image_path, dist_path)