import shutil

import time
import json
import re
import os
from xml.etree import ElementTree
from datetime import datetime

output_folder = "output"
json_files_path = "products"


def sanitize_price_and_return_as_float(price):
    updated_price = re.sub(r'[^\d]', '', price)
    return float(updated_price)


def convert_to_lowercase_with_dashes(input_string):
    underscored_string = re.sub(r'[^a-zA-Z0-9-]', '_', input_string)
    dashed_string = underscored_string.replace(" ", "-")
    lowercase_string = dashed_string.lower()

    return lowercase_string


def clean_up(html):
    return html.replace('ebecee', 'fff').replace('http:', 'https:')


def create_json_folder_if_not_exists():
    create_folder_if_not_exists(json_files_path)


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
    image_caption_elem.text = image_loc


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


def save_json_file(project_id, scraped_data):
    # Saving the data to a JSON file
    with open(json_files_path + '/' + project_id + '.json', 'w') as json_file:
        json.dump(scraped_data, json_file, indent=4)
        print("Data saved to json file")

def extract_categories(product_list):
    categories = set()
    for product in product_list:
        categories.add(product['category'])

    return list(categories)