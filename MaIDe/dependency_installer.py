# this file contains the code to check for dependencies and install them if they are not found
# in case the NIS software is on a network controlled machine, this will allow the user to install the dependencies without admin/network privileges

#import pkg_resources
import os
import glob
from pathlib import Path
import pkg_resources
from importlib import reload

def grab_predownloaded_dependencies(): 
    # This function returns a dict of strings corresponding to the included wheels.
    # open the wheel directory and loop through all the files
    file_location = os.path.dirname(os.path.abspath(__file__))
    lookin = Path("{}/wheels/".format(file_location))
    # print(lookin)
    included_wheels = glob.glob(str(lookin / "*.whl" ))
    return {os.path.basename(iw).split("-")[0].lower():iw for iw in included_wheels}

def check_avail_packages():
    # This function returns a list of strings corresponding to the packages installed in the user's system.
    reload(pkg_resources)
    return ["_".join(d.project_name.split("-")).lower() for d in pkg_resources.working_set]

def get_missing_packages(avail, predownloaded):
    # This function returns a list of strings corresponding to the packages that are not installed in the user's system.
    return [p for p in predownloaded if p not in avail]

def install_select_packages(pkgs_to_install, pkg_locations):
    # this script installs the packages in the list pkgs_to_install from the dict pkg_locations
    for pkg in pkgs_to_install:
        print("Installing {}...".format(pkg))
        os.system("pip install {} --no-index --find-links={} > NUL 2>&1".format(pkg_locations[pkg], pkg_locations[pkg]))

def install_all_included_dependencies(max_loops = 5):
    """ recursively tries to install all the dependencies
    """
    if max_loops == 0:
        raise ValueError("Max loops reached (are all required wheels included?), exiting...")
    predownloaded = grab_predownloaded_dependencies()
    avail = check_avail_packages()
    miss = get_missing_packages(avail, predownloaded)
    # print("avail",avail)
    if len(miss) > 0:
        print("missing",miss)
        install_select_packages(miss, predownloaded)
        return install_all_included_dependencies(max_loops = max_loops - 1)
    else:
        return True