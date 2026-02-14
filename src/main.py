import sys
from copy_static import copy_static_to_public, clear_dest_path
from generate_page import extract_title, generate_page, generate_pages_recursive

src_path = "./static"
dest_path = "./docs"
md_path = "./content"
template_path = "./template.html"

def main(basepath):
  print(basepath)
  with open("log.txt", "w") as f:
    f.write(f"Copying files from {src_path} to {dest_path}\n")
  clear_dest_path(dest_path)
  copy_static_to_public(src_path, dest_path)
  
  with open("log.txt", "a") as f:
    f.write(f"Generating HTML")
  generate_pages_recursive(md_path, template_path, dest_path, basepath)

    


if __name__ == "__main__":
  if len(sys.argv) > 1 :
    basepath = sys.argv[1]
  else:
    basepath = "/"
  main(basepath)