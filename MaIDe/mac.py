# mac.py
# this file contains the functions to create the mac file

import nd2
import numpy as np
import os

def construct_mac_file(template_fname, img_files, img_dict, img_suffix, output_dir,channel_mask,mac_filename):
    # this function constructs the mac file
    
    mac_contents = ""
    with open(template_fname, "r") as f:
        template = f.read().strip()
    for img_file in img_files:
        output_file = os.path.join(output_dir, os.path.basename(img_file)[:-4] + img_suffix)
        output_file = output_file.replace("/","\\")
        met = img_dict[img_file]
        img_file = img_file.replace("/","\\")
        zeros = "0.0:"*met["channelCount"]
        emissionLambda = "".join(["{:.1f}:".format(n) for n in met["emissionLambdaNms"]])
        excitationLambda = "".join(["{:.1f}:".format(n) for n in met["excitationLambdaNms"]])
        res = template.replace("$CHANNELS_ZERO",zeros)
        res = res.replace("$CHANNEL_MASK",channel_mask)
        res = res.replace("$CHANNEL_EMISSION_LAMBDA",emissionLambda)
        res = res.replace("$CHANNEL_EXCITATION_LAMBDA",excitationLambda)
        res = res.replace("$ORIGINAL_IMG",img_file)
        res = res.replace("$NEW_IMG",output_file)
        mac_contents += res + "\n"
    with open(output_dir+"\\"+mac_filename, "w+") as f:
        f.write(mac_contents)

def parse_nd2_file(img_file):
    extracted_contents = {}
    with nd2.ND2File(img_file) as ndfile:
        met = ndfile.metadata
    extracted_contents["channelCount"] = met.contents.channelCount # type: ignore
    extracted_contents["frameCount"] = met.contents.frameCount # type: ignore
    extracted_contents["channel_names"] = []
    extracted_contents["emissionLambdaNms"] = []
    extracted_contents["excitationLambdaNms"] = []
    for channel in met.channels: # type: ignore
        extracted_contents["channel_names"].append(channel.channel.name)
        extracted_contents["emissionLambdaNms"].append(channel.channel.emissionLambdaNm) 
        extracted_contents["excitationLambdaNms"].append(channel.channel.excitationLambdaNm)
    return extracted_contents

def verify_nd2_files(nd2_dict):
    channel_names = None
    first_img = None
    for img in nd2_dict:
        if channel_names is None:
            first_img = img
            channel_names = nd2_dict[img]["channel_names"]
        else:
            if channel_names != nd2_dict[img]["channel_names"]:
                print(f"Channel names do not match between images '{img}' and '{first_img}'\nReceived: {nd2_dict[img]['channel_names']}\nExpected: {channel_names}")
                print(f"Please verify all the images in the folder have the same channel names or seperate them across different folders.\n Aborting ...")
                raise ValueError("images have different channels")
    return True