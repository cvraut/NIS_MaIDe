# D:\spelioteslab\craut\python
# usage: D:\spelioteslab\craut\python D:\spelioteslab\craut\VC\NIS_MaIDe\tools\folder_diff.py

import os

def list_files_in_directory(directory):
    """List all files in the given directory, excluding subdirectories."""
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            files.append(item)
    return files

def get_latest_file(directory):
    """Get the most recently modified file in the directory."""
    latest_file = None
    latest_time = 0
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            modified_time = os.path.getmtime(item_path)
            if modified_time > latest_time:
                latest_time = modified_time
                latest_file = item
    return latest_file

def get_unique_files(folder1, folder2):
    """Get the list of files in folder1 that are not in folder2."""
    # Get the list of files in both folders
    folder1_files = set(f.split(".nd2")[0] for f in list_files_in_directory(folder1) if ".nd2" in f)
    f2_files = set(list_files_in_directory(folder2))
    # Get the latest file in folder2 to ignore it
    latest_file_folder2 = get_latest_file(folder2)
    if latest_file_folder2:
        print(f"Ignoring the latest file in Folder 2: {latest_file_folder2}")
        f2_files.discard(latest_file_folder2)  # Remove the latest file from the set

    folder2_files = set(f.split("_img_deconv")[0] for f in f2_files if "_img_deconv" in f)
    print(f"found deconvolved files for {len(folder2_files)}/{len(folder1_files)} images")
    # Find files that are only in folder1 and not in folder2
    unique_files = folder1_files - folder2_files
    
    return sorted(unique_files)

def main():
    # Input folder paths
    folder1 = input("Enter the path for Folder 1 (imgs to deconv): ").strip()
    folder2 = input("Enter the path for Folder 2 (deconv imgs): ").strip()

    # Validate folder paths
    if not os.path.isdir(folder1):
        print(f"Error: Folder 1 '{folder1}' does not exist.")
        return
    if not os.path.isdir(folder2):
        print(f"Error: Folder 2 '{folder2}' does not exist.")
        return

    # Get the unique files
    unique_files = get_unique_files(folder1, folder2)

    # Output the result
    if unique_files:
        print(f"Files found in Folder 1 but not in Folder 2:")
        for file in unique_files:
            print(file)
    else:
        print("No unique files found in Folder 1.")

if __name__ == "__main__":
    main()