import re
from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
  blocks = markdown.split('\n\n')
  filtered_blocks = []
  for block in blocks:
    if block == "":
      continue
    filtered_blocks.append(block.strip())
  return filtered_blocks

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode("div", children, None)

def block_to_html_node(block):
  block_type = block_to_block_type(block)
  if block_type == BlockType.HEADING:
    return get_heading_node(block)
  if block_type == BlockType.CODE:
    return get_code_node(block)
  if block_type == BlockType.QUOTE:
    return get_quote_node(block)
  if block_type == BlockType.ORDERED_LIST:
    return get_ol_node(block)
  if block_type == BlockType.UNORDERED_LIST:
    return get_ul_node(block)
  if block_type == BlockType.PARAGRAPH:
    return get_p_node(block)

def block_to_block_type(block):
  if re.match(r'^#{1,6}\s+.*$', block):
    return BlockType.HEADING
  elif re.match(r'^```\n[\s\S]*```$', block):
    return BlockType.CODE
  elif re.match(r'^(>.*\n?)+$', block):
    return BlockType.QUOTE
  elif re.match(r'^(-\s.*\n?)+$', block):
    return BlockType.UNORDERED_LIST
  elif re.match(r'^([0-9]\.\s+.*\n?)+$', block):
    return BlockType.ORDERED_LIST
  else:
    return BlockType.PARAGRAPH

def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)
  return children
    
def get_heading_node(block):
  match = re.match(r'^(#){1,6}', block)
  h = len(match.group(0))
  text = block[h + 1:]
  children = text_to_children(text)
  return ParentNode(f"h{h}", children)

def get_code_node(block):
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError(f"Invalid code block")
  text = block[4:-3]
  text_node = TextNode(text, TextType.TEXT)
  child = text_node_to_html_node(text_node)
  code = ParentNode("code", [child])
  return(ParentNode("pre", [code]))

def get_quote_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("invalid block quote")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode("blockquote", children)

def get_ul_node(block):
  html_items = []
  items = block.split("\n")
  for item in items:
    children = text_to_children(item[2:]) 
    html_items.append(ParentNode("li", children))
  return ParentNode("ul", html_items)

def get_ol_node(block):
  html_items = []
  items = block.split("\n")
  for item in items:
    match = re.match(r'^([0-9].\s)', item)
    text = item.replace(match.group(0), "").strip()
    if text != "":
      children = text_to_children(text)
      html_items.append(ParentNode("li", children))
  return ParentNode("ol", html_items)

def get_p_node(block):
  html_items = []
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode("p", children)