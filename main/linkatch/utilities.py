from lxml import etree, html


def _strip_text(tree: etree.ElementBase) -> etree.ElementBase:
    if tree.text is not None:
        tree.text = tree.text.strip(' ')
    if tree.tail is not None:
        tree.tail = tree.tail.strip(' ')
    for child in tree:
        _strip_text(child)
    return tree


def _clear_all_attributes(tree: etree.ElementBase) -> etree.ElementBase:
    for element in tree.iter():
        element.attrib.clear()
    return tree


def _remove_tags(tree: etree.ElementBase, tags: list[str]) -> etree.ElementBase:
    for tag in tags:
        for element in tree.xpath(f'//{tag}'):
            element.getparent().remove(element)
    return tree


def _change_tags(tree: etree.ElementBase, replacements: dict) -> etree.ElementBase:
    for target_tag, new_tag in replacements.items():
        # Find all elements matching the target tag
        for elem in tree.findall('.//' + target_tag):
            # Create a new element with the desired tag
            new_elem = html.Element(new_tag)
            # Copy text and tail from the old element
            new_elem.text, new_elem.tail = elem.text, elem.tail
            # Move all children from the old element to the new element
            for child in elem.getchildren():
                new_elem.append(child)
            # Replace the old element with the new element in the tree
            elem.getparent().replace(elem, new_elem)
    return tree


def _format_lists(tree: etree.ElementBase) -> etree.ElementBase:
    # Linkatch does not show lists - replace all lists with <p>
    ul_elements = tree.findall('.//ul')
    for ul in ul_elements:
        # For each <li> in the current <ul>
        for li in ul.findall('li'):
            new_p = etree.Element("p")
            new_p.text = " - " + li.text if li.text else ""
            ul.addprevious(new_p)
        ul.getparent().remove(ul)
    return tree


def nbn_description_to_linkatch(document: str | etree.ElementBase) -> str:
    tree = html.fromstring(document) if isinstance(document, str) else document
    tree = _strip_text(tree)
    tree = _clear_all_attributes(tree)
    tree = _remove_tags(tree, ['pre'])
    tree = _change_tags(tree, {'h1': 'strong', 'h2': 'strong', 'span': 'p'})
    tree = _format_lists(tree)
    return '\n'.join(etree.tostring(child, encoding='unicode', method='html').strip() for child in tree.iterchildren())


if __name__ == '__main__':
    document = '''
        <div>
          <h2 class="widget-title widget-title--job_listing-top job-overview-title">Overview</h2>
          <p>An exciting opportunity to join The Media Line, the dynamic American news agency covering the Middle East in a leadership capacity.</p>
          <p>We’re seeking an experienced editor with journalistic experience to manage The Media Line’s bureau and its Press and Policy Student Program, and social media output. The candidate will be the face of the agency and must have a presence for radio/television appearances.</p>
          <p>This is a unique chance to combine working in a real-time news environment and train our future journalists.</p>
          <p>Responsibilities include managing news flow and distribution as well as mentoring and editing. You will be helping to build the successful Press and Policy Program, serving as a liaison to universities.</p>
          <p>
            <strong>Requirements:</strong>
          </p>
          <ul>
            <li>Candidate must have the ability to work with management, excellent interpersonal skills, and the ability to foster teamwork.</li>
            <li>Must have a college degree, a strong journalism background, and a minimum of five years experience as a senior editor and/or reporter.</li>
            <li>Must have a strong background in knowledge of the Middle East.</li>
            <li>Multi-media is a plus.</li>
            <li>Hebrew and Arabic are also a plus.</li>
          </ul>
          <p>Please send CVs in English along with references and writing samples.</p>
          <pre style="text-align: center;">
            <span>Tell them you heard about the position from Nefesh B’Nefesh.</span>
            <span>Please do not repost.</span>
          </pre>
        </div>
    '''
    tree = html.fromstring(document)
    tree = _strip_text(tree)
    tree = _clear_all_attributes(tree)
    tree = _remove_tags(tree, ['pre'])
    tree = _change_tags(tree, {'h1': 'strong', 'h2': 'strong', 'span': 'p'})
    tree = _format_lists(tree)
    print(nbn_description_to_linkatch(tree))
    #print(etree.tostring(tree, encoding='unicode', method='html', pretty_print=True))
