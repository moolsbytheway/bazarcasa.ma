import shutil
from constants import *
import time
import csv
import os


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def print_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    print(f"Took: {elapsed_time:.2f} seconds")


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


def calculate_transport_price(dimensions):
    if not dimensions or dimensions == "":
        return 0
    try:
        parts = [float(x) for x in dimensions.split('x')]
        product = 1
        for part in parts:
            product *= (part/100)
        # Multiply by CBM_PRICE
        return product * CBM_PRICE
    except ValueError:
        return 0
