#from MaIDe import greetings
from MaIDe import dependency_installer
from MaIDe import globals
from MaIDe import folder_selector
from MaIDe import greetings
from MaIDe import db

# check last run status

def run():
    #print(globals.check_settings())
    greetings.startup_message(globals.version, globals.contact)
    greetings.welcome_message(globals.user)
    greetings.check_run_status()
    db.get_last_run_status(globals.dbfile)

if __name__ == "__main__":
    print(globals.check_settings())
    run()