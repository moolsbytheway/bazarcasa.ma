from jinja2 import Environment, FileSystemLoader, select_autoescape

output_folder = "output"
reports_folder = "output/reports"
product_files_path = "products/current.csv"

CBM_PRICE = 50000
DEFAULT_PAGE_TITLE = 'بازار كازا - توفير و توصيل منتجات الجملة إلى موريتانيا'

env = Environment(
    loader=FileSystemLoader('src/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


# Define a custom filter for formatting prices
def format_price(value):
    try:
        return '{:.2f}'.format(float(value))
    except (ValueError, TypeError):
        return value


# Add the custom filter to the environment
env.filters['format_price'] = format_price
