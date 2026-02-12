from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
  def __init__(self, text, type, url=None):
    self.text = text
    self.type = TextType(type)
    self.url = url

  def __eq__(self, other):
    return self.__dict__ == other.__dict__

  def __repr__(self):
    return f"TextNode({self.text}, {self.type}{f', {self.url}' if self.url is not None else ''})"

def text_node_to_html_node(text_node):
  if text_node.type == TextType.TEXT:
    return LeafNode(None, text_node.text)
  elif text_node.type == TextType.BOLD:
    return LeafNode("b", text_node.text)
  elif text_node.type == TextType.ITALIC:
    return LeafNode("i", text_node.text)
  elif text_node.type == TextType.CODE:
    return LeafNode("code", text_node.text)
  elif text_node.type == TextType.LINK:
    return LeafNode("a", text_node.text, {"href": text_node.url})
  elif text_node.type == TextType.IMAGE:
    return LeafNode("img", "", {
      "src" : text_node.url,
      "alt" : text_node.text
    })
  raise ValueError(f"invalid text type: {text_node.text_type}")