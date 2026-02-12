from copy_static import copy_static_to_public, clear_dest_path
from generate_page import extract_title

src_path = "./static"
dest_path = "./public"

def main():

  with open("log.txt", "w") as f:
    f.write(f"Copying files from {src_path} to {dest_path}\n")
  clear_dest_path(dest_path)
  copy_static_to_public(src_path, dest_path)

  with open("./content/index.md", "r") as md:
    extract_title(md.read())


if __name__ == "__main__":
  main()