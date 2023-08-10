# MaIDe.py
 
from MaIDe import globals
from MaIDe import folder_selector
from MaIDe import greetings
from MaIDe import db
from MaIDe import mac
from MaIDe import monitor
import os
import subprocess

# check last run status

def run():
    if globals.debug:
        print(globals.check_settings())
    greetings.startup_message(globals.version, globals.contact)
    greetings.welcome_message(globals.user)
    greetings.check_run_status()
    last_status = db.get_last_run_status(globals.dbfile)
    if globals.debug:
        print(last_status)
    job_num = last_status["job_num"] if last_status else 1
    #db.insert_run_status(globals.dbfile, job_num, "", "", 0, "test")
    resume = False
    if last_status and last_status["status_str"] == "start" and False:
        # if the last run status was start, then we need to ask the user if they want to continue
        resume = greetings.incomplete_job(last_status["macfile_loc"], last_status["time"]) == "y"
        if resume:
            # if the user wants to resume, then we need to get the nd5_dir from the db
            print("Function: Resume old job not implemented yet 😔")
            resume = False
    if not resume:
        suggested_folders = folder_selector.get_k_folders(globals.default_image_dir,globals.k_recent,globals.folder_suffix)
        nd5_dir = greetings.select_folder(suggested_folders,globals.default_image_dir,globals.img_suffix)
        # get a list of all the nd2 files in the selected directory
        nd2_files = sorted(folder_selector.get_nd5_files(nd5_dir,globals.img_suffix))
        if globals.debug:
            print("\n".join(nd2_files))
        greetings.filenum_check(nd2_files)
        nd2_file_contents = {nd2_file:mac.parse_nd2_file(nd2_file) for nd2_file in nd2_files}
        if not mac.verify_nd2_files(nd2_file_contents):
            exit(1)
        channel_choices = nd2_file_contents[nd2_files[0]]["channel_names"]
        deconv_channels_mask = greetings.select_deconvolution_channels(channel_choices)
        output_dir = nd5_dir + globals.folder_suffix
        folder_selector.create_output_dir(output_dir)
        if globals.debug:
            print("selected channels: {}".format(deconv_channels_mask))
        # get the base dir of the output folder
        output_dir_base = os.path.basename(output_dir)
        print()
        mac_template_fname = os.path.dirname(os.path.abspath(__file__))+f"/mac_templates/{globals.template_fname}"
        mac.construct_mac_file(mac_template_fname, nd2_files, nd2_file_contents, globals.img_suffix, output_dir,deconv_channels_mask,output_dir_base+globals.mac_filename_suffix)
        mac_file_location = output_dir+"/"+output_dir_base+globals.mac_filename_suffix
        greetings.mac_file_complete(mac_file_location)
        cmd = '"{}" -m "{}"'.format(globals.NIS_exec,mac_file_location)
        cmd = cmd.replace("\\","\\\\")
        if globals.debug:
            print(cmd)
        try:
            output = subprocess.Popen(cmd, shell=True)
            #print(output)
            db.insert_run_status(globals.dbfile, job_num, macfile_loc=mac_file_location, img_dir=nd5_dir, n_imgs=len(nd2_files), status_str="start")
            monitor.job_start_wh(globals, nd5_dir, mac_file_location, len(nd2_files))
            files_done,errors,time_taken = monitor.check_progress(nd2_files,output_dir,nd5_dir + globals.failed_folder_suffix, globals.progress_delay_seconds)
            monitor.job_complete_wh(globals,len(files_done),len(errors),time_taken,output_dir,nd5_dir + globals.failed_folder_suffix)
        except Exception as e:
            print(e)
            print("Launching NIS-ar failed :(\ncontact {}".format(globals.contact))
            input("Press any key to close ...")
            raise(e)
        # subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
        
    greetings.confirm_exit()
    

if __name__ == "__main__":
    print(globals.check_settings())
    run()