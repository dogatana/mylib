import re

from lxml import etree


def strip_ns_prefix(node):
    """strip namespace from tag, name and attributes"""
    # xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    # for each element returned by the above xpath query...
    for element in node.xpath(query):
        # replace element name with its local name
        element.tag = etree.QName(element).localname
        # remove prefix from attribute name
        stripped_attr = {
            re.sub(r"\{.*?\}", "", k): v for k, v in element.attrib.items()
        }
        element.attrib.clear()
        element.attrib.update(stripped_attr)


def find_first(node, xpath_str):
    results = node.xpath(xpath_str)
    if len(results) == 0:
        return None
    else:
        return results[0]


def read_xml(filename: str):
    """xml ファイルの読み込み"""
    with open(filename, "rb") as fp:
        text = fp.read()

    return etree.fromstring(text)


def read_xml_wo_namespace(filename: str):
    """xml ファイルを読み込み、namespace を削除して返す"""
    xml = read_xml(filename)
    strip_ns_prefix(xml)
    return xml
