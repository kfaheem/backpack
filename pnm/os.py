import os

# dig into directories --> subdirectories
os.walk("dir_path")

# list dir
os.listdir("dir_path")

# make dirs
os.makedirs("dir_path", exist_ok=True)  # creates subdirectories if they don't exist

# split file name and extensiomn
os.path.splitext("file_name.txt")

# get base name
os.path.basename("/dir/var/opt/file_name.txt")  # should get file_name.txt

# check if path exists
os.path.exists("file_path")

# run command
os.system("rm -rf dir")

# rename file
os.rename("from", "to")

# join paths
os.path.join("path1", "path2")

