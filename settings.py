import os

# file consisting of default MaIDe settings

options = {
    "user":"auto",
    "maid_files_loc": r"D:/spelioteslab/craut/NIS_MaIDe/MaIDe_secret/{user}/", # default location MaIDe puts db files and looks for private settings
    "default_image_dir": f"D:/spelioteslab/{os.getlogin()}/", # default location MaIDe puts images
    "bot_name": "Naz_maide🧹",
    "contact": "craut+maide@umich.edu",
    "NIS_exec": r"C:\Program Files\NIS-Elements\nis_ar.exe",
    "folder_suffix":"_deconvolved",
    "failed_folder_suffix":"_failed_deconvolution",
    "img_suffix":"_img_deconvolved",
    "debug": False,
    "k_recent":5,
    "mac_filename_suffix":"_LiCh_MaIDe.mac",
    "template_fname": "deconvolute_template.mac",
    "from_wheels":True,
    "term_size":"auto",
}