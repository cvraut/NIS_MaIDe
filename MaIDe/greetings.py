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
    prompt="""Found incomplete job at '{}' last started at '{}'.\nWould you like to resume this job? (y/n): """
    return input_validator(prompt.format(loc,time), ["y","n"])

def validate_nd5_dir(suggested,suffix):
    num_choices = set([str(i+1) for i in range(len(suggested))])
    while True:
        response = input("Choice (1-{} or path): ".format(len(num_choices)))
        if response in num_choices:
            response = suggested[int(response)-1]
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
    user_selected_dir = validate_nd5_dir(suggested,suffix)
    print(f"Searching for .nd2 files in {user_selected_dir} ...")
    return user_selected_dir

def filenum_check(nd2_files):
    print(f"Discovered {len(nd2_files)} .nd2 files.\nPreparing mac file and image directories...")

def select_deconvolution_channels(channel_choices):
    channel_choices2 = [i for i in channel_choices] + [i.strip("nm") for i in channel_choices]
    selected = []
    while True:
        response = input(f"Please select the channels to deconvolute {channel_choices} (comma separated for multiple): ")
        if "," in response:
            response = response.split(",")
        else:
            response = [response]
        for resp in response:
            resp = resp.strip()
            if resp not in channel_choices2:
                print(f"Invalid channel '{resp}', please try again.")
                break
            else:
                selected.append(channel_choices[channel_choices2.index(resp)%len(channel_choices)])
        else:
            break
    return "".join([str(int(i in selected)) for i in channel_choices])

def confirm_exit():
    print("Done! Press any key to stop MaIDe...")
    input()
    
def mac_file_complete(mac_file):
    print("Images verfied, mac file created at '{}'.\nComencing MaIDe ...".format(mac_file))