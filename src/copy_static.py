import os, shutil


def copy_static_to_public(src, dest):
  src_files = os.listdir(src)
  copied_files = []
  os.mkdir(dest)
  with open("log.txt", "a") as f:
    f.write(f"Directory contents:\n{'\n'.join(src_files)}\n")
  for file in src_files:
    file_path = os.path.join(src, file)
    dest_path = os.path.join(dest, file)
    if not os.path.isfile(file_path):
      with open("log.txt", "a") as f:
        f.write(f"Directory {file_path} is a file? {os.path.isfile(file_path)}\n")
      copy_static_to_public(file_path, dest_path)
    else:
      with open("log.txt", "a") as f:
        f.write(f"Copying {file_path} to {dest_path}\n")
      shutil.copy(file_path, dest_path)
      
      

def clear_dest_path(dest):
  if os.path.exists(dest):
    with open("log.txt", "a") as f:
      f.write(f"Directory {dest} already exists. Deleting contents...\n")
    shutil.rmtree(f"{dest}/")

  else:
    with open("log.txt", "a") as f:
      f.write(f"Directory {dest} not found. Ready to begin copy\n")