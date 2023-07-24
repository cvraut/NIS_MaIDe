# file to store the greetings functions and anything to get printed to the console

import os
from MaIDe import folder_selector

def startup_message(version, contact):
    msg = "MaIDe v" + version + " by " + contact
    print("="*len(msg)+"\n"+msg+"\n"+"="*len(msg))
    
def welcome_message(user):
    print("Hello " + user + ", welcome to MaIDe!")
    
def check_run_status():
    print("Checking last run status...")
    
def complete():
    print("Done!")

def input_validator(prompt, valid_responses):
    # simple function to validate user input
    valid_responses = [i.lower() for i in valid_responses]
    while True:
        response = input(prompt).lower()
        if response in valid_responses:
            return response
        else:
            print(f"Invalid response '{response}', please try again.")

def incomplete_job(loc,time):
    prompt="""Found incomplete job at '{}' last started at '{}'.
    Would you like to resume this job? (y/n): """
    return input_validator(prompt.format(loc,time), ["y","n"])

def validate_nd5_dir(suggested,suffix):
    num_choices = set([str(i+1) for i in range(len(suggested))])
    while True:
        response = input("Choice (1-{} or path): ".format(len(num_choices)))
        if response in num_choices:
            return suggested[int(response)-1]
        else:
            # check if the response is a folder that exists and can be read
            if os.path.exists(response) and os.access(response, os.R_OK):
                if len(folder_selector.get_nd5_files(response,ignore_suffix=suffix)) > 0:
                # check if the folder has at least one nd5 file
                    return response
                else:
                    print(f"'{response}' does not contain any nd5 files. Please try again.")
            else:
                print(f"'{response}' is not in [1-{len(num_choices)}] or is an invalid folder. Please try again.")

def select_folder(suggested,img_dir,suffix):
    print("Please select the folder containing the nd5 files to deconvolute.")
    print("Suggested Folders (recently updated folders in '{}'):".format(img_dir))
    for i in range(len(suggested)):
        print("[{}] {}".format(i+1,suggested[i]))
    return validate_nd5_dir(suggested,suffix)
    