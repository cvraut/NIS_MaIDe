# test_folder_selector.py

import os
from time import sleep
import unittest
from MaIDe import globals
from MaIDe import db
from MaIDe import folder_selector

class TestModule(unittest.TestCase):
    def test_get_k_folders(self):
        img_dir = globals.default_image_dir
        #print(img_dir)
        # create 5 folders in img_dir
        for i in range(globals.k_recent):
            try:
                os.mkdir(os.path.join(img_dir, "test_folder_{}".format(i)))
                os.mkdir(os.path.join(img_dir, "test_folder_{}{}".format(i,globals.folder_suffix)))
            except FileExistsError:
                os.rmdir(os.path.join(img_dir, "test_folder_{}".format(i)))
                os.mkdir(os.path.join(img_dir, "test_folder_{}".format(i)))
            sleep(0.1)
            
        k_folders = folder_selector.get_k_folders(img_dir,globals.k_recent,folder_suffix=globals.folder_suffix)
        # k_folders = folder_selector.get_k_folders(img_dir,3)
        # print(k_folders)
        # print(k_folders)
        for i in range(globals.k_recent):
            self.assertTrue("test_folder_{}".format(i) in k_folders[globals.k_recent-i-1])
        # remove the 5 folders created for this unit test
        for i in range(globals.k_recent):
            os.rmdir(os.path.join(img_dir, "test_folder_{}".format(i)))
            os.rmdir(os.path.join(img_dir, "test_folder_{}{}".format(i,globals.folder_suffix)))
    
    def test_get_nd5_files(self):
        # create 5 nd5 files in a test_images folder
        test_images_dir = os.path.join(globals.default_image_dir, "test_images")
        # create the test dir
        os.mkdir(test_images_dir)
        for i in range(5):
            with open(os.path.join(test_images_dir, "test_image_{}.nd2".format(i)), "w+") as f:
                f.write("test")
            with open(os.path.join(test_images_dir, "test_image_{}{}.nd2".format(i,globals.img_suffix)), "w+") as f:
                f.write("test")
        
        nd5_files = folder_selector.get_nd5_files(test_images_dir,ignore_suffix=globals.img_suffix)
        self.assertEqual(len(nd5_files), 5)
        
        # delete the img_dir and all its contents
        for f in os.listdir(test_images_dir):
            os.remove(os.path.join(test_images_dir, f))
        os.rmdir(test_images_dir)
            
        

if __name__ == "__main__":
    unittest.main()