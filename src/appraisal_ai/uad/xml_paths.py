from __future__ import annotations

from lxml import etree


def _segments(xpath: str) -> list[str]:
    p = xpath.strip()
    if not p.startswith("/"):
        msg = f"Only absolute /Root/child paths are supported, got {xpath!r}"
        raise ValueError(msg)
    parts = [s for s in p.split("/") if s]
    if not parts:
        msg = f"Empty path: {xpath!r}"
        raise ValueError(msg)
    return parts


def get_path_text(root: etree._Element, xpath: str) -> str | None:
    """Read text at an absolute child path from root (root tag must match first segment)."""
    segs = _segments(xpath)
    if root.tag != segs[0]:
        return None
    node: etree._Element = root
    for name in segs[1:]:
        child = None
        for c in node:
            if c.tag == name:
                child = c
                break
        if child is None:
            return None
        node = child
    text = (node.text or "").strip()
    return text or None


def set_path_text(root: etree._Element, xpath: str, value: str) -> None:
    """Create missing intermediate elements and set text on the leaf."""
    segs = _segments(xpath)
    if root.tag != segs[0]:
        msg = f"Root tag {root.tag!r} does not match path root {segs[0]!r}"
        raise ValueError(msg)
    node = root
    for name in segs[1:-1]:
        child = None
        for c in node:
            if c.tag == name:
                child = c
                break
        if child is None:
            child = etree.SubElement(node, name)
        node = child
    leaf_name = segs[-1]
    leaf = None
    for c in node:
        if c.tag == leaf_name:
            leaf = c
            break
    if leaf is None:
        leaf = etree.SubElement(node, leaf_name)
    leaf.text = value


def parse_xml(data: bytes) -> etree._Element:
    parser = etree.XMLParser(remove_blank_text=True, huge_tree=False)
    return etree.fromstring(data, parser=parser)


def serialize_xml(root: etree._Element) -> bytes:
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", pretty_print=True)
