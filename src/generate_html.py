import htmlmin
from collections import defaultdict

from utils import *
from sitemap_builder import *


def get_last_update_date(package):
    return package["price"]


def generate_products_list(product, root_image_path=""):
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


def generate_reports_page_html(products):
    template = env.get_template('reports.template.j2')
    last_update_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return template.render(products=products,
                           cbm_price=CBM_PRICE,
                           last_update_date=last_update_date)


def generate_html(products):
    # group by category
    by_category_products_dict = defaultdict(list)
    for item in products:
        by_category_products_dict[item["category_slug"]].append(item)

    category_slug_map = {}
    category_names = extract_field(products, "category")
    slugs = extract_field(combined_data, "category_slug")
    for i in range(len(slugs)):
        category_slug_map[slugs[i]] = category_names[i]

    by_category_products = ""
    for category, items in by_category_products_dict.items():
        by_category_products += f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{category_slug_map[category]}</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

        for item in items:
            by_category_products += generate_products_list(item)

        by_category_products += """
                </div>
            </div>
        </section>
        """

    category_pages_map = {}
    home_page_html_content = generate_home_page_html(by_category_products, slugs, category_slug_map)

    for category, items in by_category_products_dict.items():
        details_by_dest_packages_list = f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{category_slug_map[category]}</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

        for item in items:
            details_by_dest_packages_list += generate_products_list(item)

        details_by_dest_packages_list += """
                </div>
            </div>
        </section>
        """
        cat_page_title = f"بازار كازا - {category_slug_map[category]}"
        category_pages_map[category] = generate_home_page_html(details_by_dest_packages_list, slugs, category_slug_map,
                                                               category, cat_page_title)

    build_sitemap(slugs)

    # generate reports
    reports_html_content = ""
    for item in products:
        item['transport_price'] = calculate_transport_price(item['dimensions'])
    reports_html_content = generate_reports_page_html(products)

    return home_page_html_content, category_pages_map, reports_html_content


if __name__ == "__main__":
    start_time = time.time()

    combined_data = read_csv_files()
    copy_assets()
    create_folder_if_not_exists(reports_folder)

    category_slugs = extract_field(combined_data, "category_slug")

    for cat_slug in category_slugs:
        create_folder_if_not_exists(output_folder + "/html/categories/" + cat_slug)

    html_output, category_pages, reports_html = generate_html(combined_data)

    with open(reports_folder + "/index.html", 'w') as html_file:
        html_file.write(htmlmin.minify(reports_html))

    with open(output_folder + "/html/index.html", 'w') as html_file:
        html_file.write(htmlmin.minify(html_output))

    for category_slug, page_data in category_pages.items():
        with open(output_folder + "/html/categories/" + category_slug + "/index.html", 'w') as html_file:
            html_file.write(htmlmin.minify(page_data))

    print("HTML files created")

    print_elapsed_time(start_time)
