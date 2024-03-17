from lxml import html, etree


def clear_all_attributes(html_content: str) -> str:
    # content to html tree
    tree = html.fromstring(html_content)
    # clear all attributes from all elements
    for element in tree.iter():
        element.attrib.clear()
    return etree.tostring(tree, encoding='unicode', method='html')
