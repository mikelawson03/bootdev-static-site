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

def text_to_children(block, block_type):
  if block_type == BlockType.CODE:
    return (block_type, [TextNode(block, TextType.CODE)])
  if block_type == BlockType.PARAGRAPH:
    block = block.replace('\n', ' ')
  nodes = text_to_textnodes(block)
  return (block_type, nodes)
  

def get_parent_tag(block_node):
  block_type = block_node[0]
  if block_type == BlockType.UNORDERED_LIST:
    return "ul"
  if block_type == BlockType.ORDERED_LIST:
    return "ol"
  if block_type == BlockType.PARAGRAPH:
    return "p"

def get_leaf_nodes(nodes):
  leaf_nodes = []
  for node in nodes:
    leaf_nodes.append(text_node_to_html_node(node))
  return leaf_nodes
    
def get_code_node(block_node):
  node_text = block_node[1][0].text.replace("```", "").lstrip()
  leaf_nodes = [LeafNode("code", node_text)]
  return("pre", leaf_nodes)


def get_heading_node(block_node):
  match = re.match(r'^(#){1,6}', block_node[1][0].text)
  tag = f"h{len(match.group(0))}"
  block_node[1][0].text = block_node[1][0].text.replace(match.group(0), "").lstrip()
  leaf_nodes = get_leaf_nodes(block_node[1])
  return (tag, leaf_nodes)

def get_quote_node(block_node):
  leaf_nodes = []
  block_node[1][0].text = block_node[1][0].text.replace(">", "").strip()
  for node in block_node[1]:
    leaf_nodes.append(text_node_to_html_node(node))
  return ("blockquote", leaf_nodes)

def get_ul_node(block_node):
  leaf_nodes = []
  nodes = block_node[1][0].text.split("-")
  for node in nodes:
    if node != "":
      leaf_nodes.append(LeafNode("li", node.strip()))
  return("ul", leaf_nodes)

def get_ol_node(block_node):
  leaf_nodes = []
  nodes = block_node[1][0].text.split("\n")
  for node in nodes:
    match = re.match(r'^([0-9].\s)', node)
    node = node.replace(match.group(0), "").strip()
    if node != "":
      leaf_nodes.append(LeafNode("li", node))
  return("ol", leaf_nodes)

def get_p_node(block_node):
  leaf_nodes = []
  nodes = block_node[1]
  for node in nodes:
    leaf_nodes.append(text_node_to_html_node(node))
  return("p", leaf_nodes)


def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  text_nodes = []
  block_nodes = []
  html_string = ""
  for block in blocks:
    block_type = block_to_block_type(block)
    text_nodes.append(text_to_children(block, block_type))
  for block_node in text_nodes:
    node_type = block_node[0]
    tag = ""
    children = ""
    if node_type == BlockType.CODE:
      tag, children = get_code_node(block_node)
    if node_type == BlockType.HEADING:
      tag, children = get_heading_node(block_node)
    elif node_type == BlockType.QUOTE:
      tag, children = get_quote_node(block_node)
    elif node_type == BlockType.UNORDERED_LIST:
      tag, children = get_ul_node(block_node)
    elif node_type == BlockType.ORDERED_LIST:
      tag, children = get_ol_node(block_node)
    elif node_type == BlockType.PARAGRAPH:
      tag, children = get_p_node(block_node)
    block_nodes.append(ParentNode(tag, children))
  return ParentNode("div", block_nodes)