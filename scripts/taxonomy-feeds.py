"""Build RSS indexes of taxonomy terms from Zola's per-term feeds."""

from argparse import ArgumentParser
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

ATOM = "http://www.w3.org/2005/Atom"


def write_index(directory: Path, root_channel: ET.Element) -> None:
    items = []
    for feed in sorted(directory.glob("*/index.xml")):
        channel = ET.parse(feed).getroot().find("channel")
        title, _, _ = channel.findtext("title").partition(" on ")
        link = channel.findtext("link")
        date = channel.findtext("lastBuildDate")
        item = ET.Element("item")
        for tag, value in (("title", title), ("link", link), ("pubDate", date), ("guid", link)):
            ET.SubElement(item, tag).text = value
        ET.SubElement(item, "description")
        items.append(item)

    items.sort(key=lambda item: parsedate_to_datetime(item.findtext("pubDate")), reverse=True)
    name = directory.name.title()
    site_title = root_channel.findtext("title")
    url = root_channel.findtext("link") + directory.name + "/"

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for tag, value in (
        ("title", f"{name} on {site_title}"),
        ("link", url),
        ("description", f"Recent content in {name} on {site_title}"),
        ("generator", root_channel.findtext("generator")),
        ("language", root_channel.findtext("language")),
    ):
        ET.SubElement(channel, tag).text = value

    if items:
        ET.SubElement(channel, "lastBuildDate").text = items[0].findtext("pubDate")
    ET.SubElement(
        channel, f"{{{ATOM}}}link", href=url + "index.xml", rel="self", type="application/rss+xml"
    )
    channel.extend(items)
    ET.indent(rss)
    ET.ElementTree(rss).write(directory / "index.xml", encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path, help="directory containing the built site")
    site = parser.parse_args().site

    ET.register_namespace("atom", ATOM)
    root_channel = ET.parse(site / "index.xml").getroot().find("channel")
    if root_channel is None:
        parser.exit(1, f"No RSS channel in {site / 'index.xml'}\n")

    for taxonomy in ("authors", "tags"):
        directory = site / taxonomy
        if directory.is_dir():
            write_index(directory, root_channel)


if __name__ == "__main__":
    main()
