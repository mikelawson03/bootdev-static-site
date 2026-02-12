import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  
  ## process nodes in list
  for node in old_nodes:
    if node.type != TextType.TEXT:
      new_nodes.append(node)
    else:
      if node.text.count(delimiter) % 2 != 0:
        raise Exception("invalid markup. missing closing delimiter")
      
      split_node = node.text.split(delimiter)

      nodes = []
      for i in range(0, len(split_node)):
        if split_node[i] == "":
          continue
        if i % 2 == 0:
          nodes.append(TextNode(split_node[i], TextType.TEXT))
        else:
          nodes.append(TextNode(split_node[i], text_type))
      new_nodes.extend(nodes)
  return new_nodes

def extract_markdown_images(text):
  matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return matches

def extract_markdown_links(text):
  matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  return matches

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.type != TextType.TEXT:
      new_nodes.append(node)
      continue
    else:
      original_text = node.text
      extracted_images = extract_markdown_images(original_text)
      if len(extracted_images ) == 0:
        new_nodes.append(node)
        continue
      for image in extracted_images:
        sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
        if len(sections) != 2:
          raise ValueError("invalid markdown, image section not closed")
        if sections[0] != "":
          new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        original_text = sections[1]
      if original_text != "":
        new_nodes.append(TextNode(original_text, TextType.TEXT))
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.type != TextType.TEXT:
      new_nodes.append(node)
      continue
    else:
      original_text = node.text
      extracted_links = extract_markdown_links(original_text)
      if len(extracted_links) == 0:
        new_nodes.append(node)
        continue
      for link in extracted_links:
        sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
        if len(sections) != 2:
          raise ValueError("invalid markdown, link section not closed")
        if sections[0] != "":
          new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        original_text = sections[1]
      if original_text != "":
        new_nodes.append(TextNode(original_text, TextType.TEXT))
  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  return nodes