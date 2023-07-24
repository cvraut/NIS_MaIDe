# MaIDe.py
 
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
    last_status = db.get_last_run_status(globals.dbfile)
    if globals.debug:
        print(last_status)
    job_num = last_status["job_num"] if last_status else 1
    #db.insert_run_status(globals.dbfile, job_num, "", "", 0, "test")
    resume = False
    if last_status and last_status["status"] == "start":
        # if the last run status was start, then we need to ask the user if they want to continue
        resume = greetings.incomplete_job(last_status["loc"], last_status["time"]) == "y"
        if resume:
            # if the user wants to resume, then we need to get the nd5_dir from the db
            print("Function: Resume old job not implemented yet 😔")
    if not resume:
        # nd5_dir = folder_selector.select_folder()
        pass

if __name__ == "__main__":
    print(globals.check_settings())
    run()