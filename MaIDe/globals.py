import os
import sys
sys.path.append('../')
import settings
from json import load, dump
#from MaIDe import dependency_installer

# things to get the linter to calm down
# in the future prolly replace these with defaults 🤔 ...
version = ""
maid_files_loc = ""
dbfile = ""
default_image_dir = ""
contact = ""
user = ""
debug = ""
k_recent = 0
folder_suffix = ""
img_suffix = ""
mac_filename_suffix = ".mac"
template_fname = ""
NIS_exec = ""
term_size = ""

def check_settings():
    # This function checks the settings.py file for any errors.
    if settings.options["user"] == "auto":
        settings.options["user"] = os.getlogin()
    if "{user}" in settings.options["maid_files_loc"]:
        settings.options["maid_files_loc"] = settings.options["maid_files_loc"].format(user = settings.options["user"])
    if "{user}" in settings.options["default_image_dir"]:
        settings.options["default_image_dir"] = settings.options["default_image_dir"].format(user = settings.options["user"])
    if not os.path.exists(settings.options["maid_files_loc"]):
        print("MaIDe files location does not exist, creating...")
        os.makedirs(settings.options["maid_files_loc"],exist_ok=True)
    if not os.path.exists(settings.options["default_image_dir"]):
        print("MaIDe default image directory does not exist, creating...")
        os.makedirs(settings.options["default_image_dir"],exist_ok=True)
    if settings.options["term_size"] == "auto":
        settings.options["term_size"] = os.get_terminal_size()[0]
    return settings.options

checked_settings = check_settings()
# release the checked settings to global namespace
for k in checked_settings:
    globals()[k] = checked_settings[k]

private_settings_default = {"webhook_urls":{},"dbfile":maid_files_loc+"\\maide.db"}

private_fname = maid_files_loc + "private_settings.json"
print(private_fname)

def grab_private_settings():
    # This function looks in the MaIDe files location for a private_settings.json and returns the contents as a dict.
    # if the file does not exist, it returns an empty dict.
    
    # check if the file exists
    if not os.path.exists(private_fname):
        return {}
    
    with open(private_fname, "r") as f:
        return load(f)
    
def write_private_settings(private_settings):
    # this write the private settings to the private_settings.json file
    with open(private_fname, "w+") as f:
        dump(private_settings, f)

private_settings = grab_private_settings()

if len(private_settings) == 0:
    print("No private settings found, creating...")
    write_private_settings(private_settings_default)
    private_settings = grab_private_settings()

for k in private_settings:
    globals()[k] = private_settings[k]    

try:
    import nd2
except ModuleNotFoundError:
    print("missing nd2 library, installing dependencies...")
    dependency_installer.install_all_included_dependencies()

# grab version from the .toml file
with open(os.path.dirname(os.path.abspath(__file__))+"\\pyproject.toml", "r") as f:
    for line in f:
        if "version" in line:
            version = line.split("=")[1].replace('"','').strip()
            break