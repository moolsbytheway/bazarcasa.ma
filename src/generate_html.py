import htmlmin
from collections import defaultdict

from utils import *
from sitemap_builder import *


def generate_product_card(product, root_image_path=""):
    price_formatted = float(product['price'])
    price_formatted = f"{price_formatted:,.0f}"

    template = env.get_template('fragment/product_card.template.j2')
    return template.render(product=product, price_formatted=price_formatted,
                           show_price=product['price'] != "0",
                           root_image_path=root_image_path)


def generate_home_page_html(by_category_packages, featured_items_html, categories, cat_map, filter_on_category=None,
                            page_title=DEFAULT_PAGE_TITLE):
    template = env.get_template('home_page.template.j2')
    last_update_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return template.render(by_category_packages=by_category_packages,
                           categories=categories,
                           featured_items_html=featured_items_html,
                           filter_on_category=filter_on_category,
                           cat_map=cat_map,
                           page_title=page_title,
                           last_update_date=last_update_date)


def generate_html(products):
    # group by category
    by_category_products_dict = defaultdict(list)
    for item in products:
        by_category_products_dict[item["category_slug"]].append(item)

    slugs = extract_field(combined_data, "category_slug")

    category_slug_map = {
        "dates": "تمور",
        "barber": "الحلاقة",
        "cosmetics": "منتجات التجميل"
    }

    by_category_products = ""
    for category, items in by_category_products_dict.items():
        by_category_products += f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{category_slug_map[category]}</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

        for item in sorted(items, key=lambda x: (int(x['cat_id']), int(x['id'])), reverse=True):
            by_category_products += generate_product_card(item)

        by_category_products += """
                </div>
            </div>
        </section>
        """

    featured_items = [item for item in products if item['featured'] == "1"]
    featured_items_html = f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">منتجات مميزة</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

    for featured_item in featured_items:
        featured_items_html += generate_product_card(featured_item)

    featured_items_html += """
            </div>
        </div>
    </section>
    """

    home_page_html_content = generate_home_page_html(by_category_products, featured_items_html, slugs,
                                                     category_slug_map)

    category_pages_map = {}
    for category, items in by_category_products_dict.items():
        details_by_dest_products_list = f"""
                <section class="w-full" style="padding-top:20px;padding-bottom:40px;">
        <div class="container px-4 md:px-6">
        <h1 style="color:#cd8454" class="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">{category_slug_map[category]}</h1>
        <div style="flex-wrap: wrap" class="flex justify-items-center gap-6 mt-8">
        """

        for item in sorted(items, key=lambda x: (int(x['cat_id']), int(x['id'])), reverse=True):
            details_by_dest_products_list += generate_product_card(item)

        details_by_dest_products_list += """
                </div>
            </div>
        </section>
        """
        cat_page_title = f"بازار كازا - {category_slug_map[category]}"
        category_pages_map[category] = generate_home_page_html(details_by_dest_products_list, "", slugs,
                                                               category_slug_map,
                                                               category, cat_page_title)

    build_sitemap(slugs)

    return home_page_html_content, category_pages_map


if __name__ == "__main__":
    start_time = time.time()

    combined_data = read_csv_files()
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
