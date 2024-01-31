import shutil

import time
import csv
import os
from xml.etree import ElementTree
from datetime import datetime

output_folder = "output"
product_files_path = "products/current.csv"


def create_folder_if_not_exists(folder_path, path_suffix=""):
    if not os.path.exists(folder_path + path_suffix):
        os.makedirs(folder_path + path_suffix)


def print_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    print(f"Took: {elapsed_time:.2f} seconds")


def add_url_to_sitemap(sitemap_root, loc, image_loc):
    current_datetime = datetime.utcnow()
    lastmod = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    url = ElementTree.SubElement(sitemap_root, "url")

    loc_elem = ElementTree.SubElement(url, "loc")
    loc_elem.text = loc

    lastmod_elem = ElementTree.SubElement(url, "lastmod")
    lastmod_elem.text = lastmod

    image_elem = ElementTree.SubElement(url, "image:image")

    image_loc_elem = ElementTree.SubElement(image_elem, "image:loc")
    image_loc_elem.text = image_loc

    image_caption_elem = ElementTree.SubElement(image_elem, "image:caption")
    image_caption_elem.text = "بازار كازا - توفير و توصيل منتجات الجملة إلى موريتانيا"


def copy_assets():
    source_folder = 'src/public'
    destination_folder = 'output/html'

    os.makedirs(destination_folder, exist_ok=True)

    for item in os.listdir(source_folder):
        source = os.path.join(source_folder, item)
        destination = os.path.join(destination_folder, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)


def extract_field(product_list, field_name):
    categories = set()
    for product in product_list:
        categories.add(product[field_name])

    return list(categories)


def read_csv_files():
    try:
        with open(os.path.join(product_files_path), mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)
            # print(data)
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
