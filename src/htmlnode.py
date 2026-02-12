class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    html_string = ""
    if self.props:
      for x in self.props:
        html_string += f' {x}="{self.props[x]}"'
    return html_string

  def __repr__(self):
    return f"HTMLNode: tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("invalid HTML: no value")
    if self.tag is None:
      return self.value
    if self.tag != "img":
      return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    if self.tag == "img":
      return f"<{self.tag}{self.props_to_html()} />"

  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props = None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("invalid HTML: no tag")
    if self.children is None:
      raise ValueError("all parent nodes require children")
    substring = ""
    for child in self.children:
        substring += child.to_html()
    return f"<{self.tag}{self.props_to_html()}>{substring}</{self.tag}>"


