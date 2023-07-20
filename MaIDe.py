#from MaIDe import greetings
from MaIDe import dependency_installer
from MaIDe import globals

if __name__ == "__main__":
    print(globals.check_settings())
    # greetings.startup_message()
    # predownloaded = dependency_installer.grab_predownloaded_dependencies()
    # print(predownloaded)
    # avail = dependency_installer.check_avail_packages()
    # print(avail)
    # for i in range(5):
    #     predownloaded = dependency_installer.grab_predownloaded_dependencies()
    #     print(predownloaded)
    #     avail = dependency_installer.check_avail_packages()
    #     print(avail)
    #     miss = dependency_installer.get_missing_packages(avail, predownloaded)
    #     if len(miss) == 0:
    #         break
    #     dependency_installer.install_select_packages(miss, predownloaded)
    # else:
    #     raise ValueError("Max loops reached (are all required wheels included?), exiting...")