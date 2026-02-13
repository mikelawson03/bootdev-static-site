import re, os
from block_markdown import markdown_to_html_node
from pathlib import Path

dir_path_content = "./content"
dest_dir_path = "./public"
template_path = "./template.html"

def extract_title(markdown):
  match = re.match(r'#\s+.*\n', markdown)
  if match:
    h1 = match.group(0).replace("#", "").strip()
    return h1
  else:
    raise Exception("H1 required in markdown and none was found")

def generate_page(from_path, template_path, dest_path):
  generate_message = f"Generating page from {from_path} to dest_path using {template_path}\n"
  with open("log.txt", "a") as f:
    f.write(generate_message)
  check_path = Path(dest_path)
  if not check_path.is_dir():
    with open("log.txt", "a") as f:
      f.write(f"Directory {dest_path} does not yet exist. Creating...\n")
    check_path.mkdir(parents=True)
  with open(from_path, "r") as f:
    md = f.read()
  with open(template_path, "r") as f:
    template = f.read()
  html_string = markdown_to_html_node(md).to_html()
  title = extract_title(md)
  template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
  index_path = os.path.join(dest_path, "index.html")
  with open(index_path, "w") as f:
    f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  src_files = os.listdir(dir_path_content)
  dest_file_path = dest_dir_path
  with open("log.txt", "a") as f:
    f.write(f"Looking for MD files in {dir_path_content}")
    f.write(f"Directory contents: \n{'\n'.join(src_files)}\n")
  for file in src_files:
    src_file_path = os.path.join(dir_path_content, file)
    if not os.path.isfile(src_file_path):
      dest_file_path = os.path.join(dest_dir_path, file)
      with open("log.txt", "a") as f:
        f.write(f"Path {src_file_path} is a directory. Checking contents...\n")
        generate_pages_recursive(src_file_path, template_path, dest_file_path)
    elif not src_file_path.endswith(".md"):
      with open("log.txt", "a") as f:
        f.write(f"File {src_file_path} is not a valid markdown file")
        raise Exception(f"Invalid markdown file: {src_file_path}")
    else:
      with open("log.txt", "a") as f:
        f.write(f"MD file found. Calling generate_page({src_file_path}, {template_path}, {dest_dir_path})\n")
      generate_page(src_file_path, template_path, dest_file_path)
    
generate_pages_recursive(dir_path_content, template_path, dest_dir_path)