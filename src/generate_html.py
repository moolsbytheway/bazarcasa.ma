import xml.etree.ElementTree as ET
import htmlmin
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils import *

env = Environment(
    loader=FileSystemLoader('src/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

combined_data = []

# Read each JSON file and add its contents to combined_data
for filename in os.listdir(json_files_path):
    if filename.endswith('.json'):
        with open(os.path.join(json_files_path, filename), 'r') as file:
            data = json.load(file)
            combined_data.extend(data)


# Function to read JSON data
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def get_last_update_date(package):
    return package["price"]


def generate_packages_list(product, root_image_path=""):
    price_formatted = float(product['price'])
    price_formatted = f"{price_formatted:,.0f} UM"

    template = env.get_template('fragment/packages_list.template.j2')
    return template.render(product=product, price_formatted=price_formatted,
                           root_image_path=root_image_path)


def generate_home_page_html(by_category_packages, categories):
    template = env.get_template('home_page.template.j2')
    last_update_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return template.render(by_category_packages=by_category_packages,
                           categories=categories,
                           last_update_date=last_update_date)


def build_sitemap():
    sitemap_root = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    sitemap_root.set("xmlns:image", "http://www.google.com/schemas/sitemap-image/1.1")

    add_url_to_sitemap(sitemap_root,
                       "https://www.bazarcasa.ma/",
                       "https://www.bazarcasa.ma/img/logo.png")

    tree = ET.ElementTree(sitemap_root)
    tree.write(output_folder + "/html/sitemap.xml", encoding="utf-8", xml_declaration=True)


def generate_html(packages):
    build_sitemap()

    # group by category
    by_category_packages = defaultdict(list)
    for item in packages:
        by_category_packages[item["category"]].append(item)

    categories = extract_categories(packages)

    by_dest_packages_list = ""
    for category, items in by_category_packages.items():
        by_dest_packages_list += f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{category}</h1>
        <div class="grid grid-cols-4 gap-6 mt-8">
        """

        for item in items:
            by_dest_packages_list += generate_packages_list(item)

        by_dest_packages_list += """
                </div>
            </div>
        </section>
        """

    home_page_html_content = generate_home_page_html(by_dest_packages_list, categories)

    return home_page_html_content


if __name__ == "__main__":
    start_time = time.time()

    copy_assets()

    html_output = generate_html(combined_data)

    with open(output_folder + "/html/index.html", 'w') as html_file:
        html_file.write(htmlmin.minify(html_output))

    print("HTML file created")

    print_elapsed_time(start_time)
