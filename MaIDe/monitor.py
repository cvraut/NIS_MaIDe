# monitor.py
# this file consists of code related to monitoring the MaIDe run
# it also consists of the code for the webhook

import requests #dependency
from datetime import datetime

def job_start_wh(globals, img_dir, mac_file, n_images):
    wh(globals,
       "Job start🏃‍♂️ ...",
       "Starting to deconvolute {} images".format(n_images),
       "img directory: '{}'\nmac_file: '{}'".format(img_dir,mac_file))
    
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
            result = requests.post(url, json = data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                if globals.debug:
                    print("Payload delivered successfully to {}, code {}.".format(sname,result.status_code))


