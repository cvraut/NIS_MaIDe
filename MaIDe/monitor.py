# monitor.py
# this file consists of code related to monitoring the MaIDe run
# it also consists of the code for the webhook

import requests #dependency
from datetime import datetime
from filecmp import cmp
from time import sleep
from MaIDe import folder_selector
import os
import shutil

def job_start_wh(globals, img_dir, mac_file, n_images):
    wh(globals,
       "Job start 🏃‍♂️ ...",
       "Starting to deconvolute {} images".format(n_images),
       "img directory: `{}`\nmac_file: `{}`".format(img_dir,mac_file))
    
def job_complete_wh(globals, n_images, n_errors, time_taken, output_dir,failed_dir):
    desc = "{}/{} images successfully deconvoluted in {} seconds\nDeconvolved images found in {}".format(n_images-n_errors,n_images,time_taken,output_dir)
    if n_errors > 0:
        desc+="\nFailed images copied to `{}`".format(failed_dir)
    wh(globals,
       "Job end 🏁 ...",
       "Finished deconvoluting {} images".format(n_images),
       desc)
    
def error_wh(globals,exception):
    desc = f"traceback: {e.traceback}"
    title = "MaIDe threw an Exception"
    content = f"exception: {e.message}"
    wh(globals,
       title,
       content,
       desc)
    raise e
    
def wh(globals,title="🧪 testing...",content="wh was called with default params",description=""):
    data = {
        "content" : title,
        "username" : globals.bot_name
    }

    #leave this out if you dont want an embed
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [ # type: ignore
        {
            "description" : f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'+ description,
            "title" : content
        }
    ]
    if globals.webhook_urls:
        for sname in globals.webhook_urls:
            url = globals.webhook_urls[sname]
            try:
                result = requests.post(url, json = data)
                result.raise_for_status()
            except requests.exceptions.ConnectionError as err:
                if globals.debug:
                    print("no connection, so webhook failed to update")
                break
            except requests.exceptions.HTTPError as err:
                print(err)
                break
            except Exception as e:
                print("caught excep!")
                raise e
        else:
            if globals.debug:
                print("Payload delivered successfully to {}, code {}.".format(sname,result.status_code))

def verify_deconvolution(img1,img2):
    # this function compares the two images and returns False if they are the same
    return cmp(img1,img2)

def check_progress(files_to_deconv,output_dir,failed_dir,delay_seconds):
    #print(output_dir)
    last_complete_time = [datetime.now()]
    time_taken = []
    #print(files_to_deconv)
    files_done = {}
    prev_done = -1
    errors = set()
    ETR = "ETR: unknown"
    while len(files_to_deconv) != len(files_done):
        nd2_in_output = folder_selector.get_nd5_files(output_dir,"")
        #print(nd2_in_output)
        if len(files_done) != prev_done:
            print("checking progress {}/{} ({})".format(len(files_done),len(files_to_deconv),ETR))
            prev_done = len(files_done)
        for nd2 in nd2_in_output:
            if nd2 not in files_done:
                for file in files_to_deconv:
                    fname = os.path.basename(file)[:-4]
                    if fname == os.path.basename(nd2)[:len(fname)]:
                        files_done[file] = nd2
                        if cmp(file,nd2):
                            errors.add(nd2)
                            print(f"noticed deconvolution error with {nd2} moving file to {failed_dir}...")
                            # move the nd2 file
                            if not os.path.exists(failed_dir):
                                os.mkdir(failed_dir)
                            if os.path.exists(nd2):
                                new_filename = fname+".nd2"
                                destination_file = os.path.join(failed_dir, new_filename)
                                shutil.move(nd2, destination_file)
                            if os.path.exists(nd2) and os.access(nd2, os.W_OK):
                                os.remove(nd2)
                        else:
                            pass
                                               
                if len(files_done) != prev_done:
                    last_complete_time.append(datetime.now())
                    time_taken.append((last_complete_time[-1] - last_complete_time[-2]).seconds)
                    time_remaining = round(sum(time_taken)*(len(files_to_deconv)/len(files_done)) - sum(time_taken))
                    ETR = "ETR: {} min {} seconds, last img took {} seconds".format(time_remaining//60,time_remaining%60,time_taken[-1])        
        sleep(int(delay_seconds))
    print(f"All {len(files_to_deconv)} files passed through deconvolution. Success rate: {len(files_done)-len(errors)}/{len(files_to_deconv)} ({round(100*(len(files_done)-len(errors))/len(files_to_deconv))}%)")
    return files_done,errors, sum(time_taken)
