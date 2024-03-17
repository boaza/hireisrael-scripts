from lxml import etree, html
from lxml.html import fromstring, tostring


def reformat_job_description(self, html_content):
    tree = fromstring(html_content)
    # Linkatch does not show lists - replace with spans
    ul_elements = tree.findall('.//ul')

    for ul in ul_elements:
        prev_element = ul.getprevious()
        # For each <li> in the current <ul>
        for li in ul.findall('li'):
            # Create a new <span> element with "-" prefix
            new_span = etree.Element("span")
            new_span.text = "- " + li.text if li.text else ""
            # Insert the new <span> element right after the previous element or <ul> itself if it's the first
            if prev_element is not None:
                prev_element.addnext(new_span)
                prev_element = new_span
            else:
                ul.addprevious(new_span)
                prev_element = new_span

            # Add a <br> after the <span> for line break, except for the last item
            br = etree.SubElement(prev_element, "br")

        # Remove the <ul> element from the tree
        ul.getparent().remove(ul)

    return tostring(tree, pretty_print=False, method="html", encoding='unicode').strip()
