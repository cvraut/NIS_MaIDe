# folder selector

import os

def get_all_folders(dirs,folder_suffix):
    # this function looks into the dirs directory and returns all the subdirectories along with their modified time
    # this function will ignore any folders ending with the folder suffix from settings.py
    if not os.path.isdir(dirs):
        return []
    # print(dirs)
    found_subdirs = []
    for d in os.listdir(dirs):
        if os.path.isdir(os.path.join(dirs, d)) and os.access(os.path.join(dirs, d), os.R_OK) and not d.endswith(folder_suffix):
            found_subdirs.append(os.path.join(dirs, d))
            # print(os.path.join(dirs, d))
    dirs = [(os.path.join(dirs, d), os.path.getmtime(os.path.join(dirs, d))) for d in found_subdirs]
    dirs.sort(key=lambda x: x[1], reverse=True)
    return dirs

def get_k_folders(dir,k,folder_suffix):
    # this function looks into the dir folder and returns the k most recent subdirectories by modified time
    return [d for d,k in sorted(get_all_folders(dir,folder_suffix),key=lambda x: x[1], reverse=True)[:k]]

def get_nd5_files(dir,ignore_suffix):
    # this function returns a list of all the nd5 files in the specified dir directory
    if not os.path.isdir(dir):
        return []
    else:
        return [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and os.path.splitext(f)[1] == ".nd2" and not f[:-4].endswith(ignore_suffix)]
    
def create_output_dir(output_dir):
    # this function creates the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)