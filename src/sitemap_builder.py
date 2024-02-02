import xml.etree.ElementTree as ET
from datetime import datetime

from constants import *


def build_sitemap(categories):
    sitemap_root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    sitemap_root.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")

    add_url_to_sitemap(sitemap_root,
                       "https://www.bazarcasa.ma/",
                       "https://www.bazarcasa.ma/img/logo.png")

    for category in categories:
        add_url_to_sitemap(sitemap_root,
                           "https://www.bazarcasa.ma/categories/" + category,
                           "https://www.bazarcasa.ma/img/logo.png")

    tree = ET.ElementTree(sitemap_root)
    tree.write(output_folder + "/html/sitemap.xml", encoding="utf-8", xml_declaration=True)


def add_url_to_sitemap(sitemap_root, loc, image_loc):
    current_datetime = datetime.utcnow()
    lastmod = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    url = ET.SubElement(sitemap_root, "url")

    loc_elem = ET.SubElement(url, "loc")
    loc_elem.text = loc

    lastmod_elem = ET.SubElement(url, "lastmod")
    lastmod_elem.text = lastmod

    image_elem = ET.SubElement(url, "image:image")

    image_loc_elem = ET.SubElement(image_elem, "image:loc")
    image_loc_elem.text = image_loc

    image_caption_elem = ET.SubElement(image_elem, "image:caption")
    image_caption_elem.text = "بازار كازا - توفير و توصيل منتجات الجملة إلى موريتانيا"
