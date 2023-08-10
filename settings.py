# file consisting of default MaIDe settings

options = {
    "user":"auto",
    "maid_files_loc": r"C:/Users/{user}/Desktop/NIS_MaIDe/MaIDe_secret/", # default location MaIDe puts db files and looks for private settings
    "default_image_dir": r"C:/Users/{user}/Documents/", # default location MaIDe puts images
    "bot_name": "craut_maide_dev🧹",
    "contact": "craut+maide@umich.edu",
    "NIS_exec": r"C:\Program Files\NIS-Elements\nis_ar.exe",
    "folder_suffix":"_deconvolved",
    "failed_folder_suffix":"_failed_deconvolution",
    "img_suffix":"_img_deconvolved",
    "debug": True,
    "k_recent":5,
    "mac_filename_suffix":"_LiCh_MaIDe.mac",
    "template_fname": "deconvolute_template.mac",
    "from_wheels":True,
    "term_size":"auto",
    "progress_delay_seconds":2, # 15 seconds is better for the machine, but worse for the human
}