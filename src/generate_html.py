import xml.etree.ElementTree as ET
import htmlmin
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils import *

DEFAULT_PAGE_TITLE = 'بازار كازا - توفير و توصيل منتجات الجملة إلى موريتانيا'

env = Environment(
    loader=FileSystemLoader('src/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

combined_data = read_csv_files()


def get_last_update_date(package):
    return package["price"]


def generate_packages_list(product, root_image_path=""):
    price_formatted = float(product['price'])
    price_formatted = f"{price_formatted:,.0f}"

    template = env.get_template('fragment/packages_list.template.j2')
    return template.render(product=product, price_formatted=price_formatted,
                           show_price=product['price'] != "0",
                           root_image_path=root_image_path)


def generate_home_page_html(by_category_packages, categories, cat_map, filter_on_category=None,
                            page_title=DEFAULT_PAGE_TITLE):
    template = env.get_template('home_page.template.j2')
    last_update_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return template.render(by_category_packages=by_category_packages,
                           categories=categories,
                           filter_on_category=filter_on_category,
                           cat_map=cat_map,
                           page_title=page_title,
                           last_update_date=last_update_date)


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


def generate_html(packages):
    # group by category
    by_category_packages = defaultdict(list)
    for item in packages:
        by_category_packages[item["category_slug"]].append(item)

    cat_map = {}
    category_names = extract_field(packages, "category")
    slugs = extract_field(combined_data, "category_slug")
    for i in range(len(slugs)):
        cat_map[slugs[i]] = category_names[i]

    by_dest_packages_list = ""
    for category, items in by_category_packages.items():
        by_dest_packages_list += f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{cat_map[category]}</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

        for item in items:
            by_dest_packages_list += generate_packages_list(item)

        by_dest_packages_list += """
                </div>
            </div>
        </section>
        """

    category_pages_map = {}
    home_page_html_content = generate_home_page_html(by_dest_packages_list, slugs, cat_map)

    for category, items in by_category_packages.items():
        details_by_dest_packages_list = f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{cat_map[category]}</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

        for item in items:
            details_by_dest_packages_list += generate_packages_list(item)

        details_by_dest_packages_list += """
                </div>
            </div>
        </section>
        """
        cat_page_title = f"بازار كازا - {cat_map[category]}"
        category_pages_map[category] = generate_home_page_html(details_by_dest_packages_list, slugs, cat_map,
                                                               category, cat_page_title)

    build_sitemap(slugs)

    return home_page_html_content, category_pages_map


if __name__ == "__main__":
    start_time = time.time()

    copy_assets()

    category_slugs = extract_field(combined_data, "category_slug")

    for cat_slug in category_slugs:
        create_folder_if_not_exists(output_folder + "/html/categories/" + cat_slug)

    html_output, category_pages = generate_html(combined_data)

    with open(output_folder + "/html/index.html", 'w') as html_file:
        html_file.write(htmlmin.minify(html_output))

    for category_slug, page_data in category_pages.items():
        with open(output_folder + "/html/categories/" + category_slug + "/index.html", 'w') as html_file:
            html_file.write(htmlmin.minify(page_data))

    print("HTML files created")

    print_elapsed_time(start_time)
