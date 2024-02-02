from jinja2 import Environment, FileSystemLoader, select_autoescape

output_folder = "output"
product_files_path = "products/current.csv"

DEFAULT_PAGE_TITLE = 'بازار كازا - توفير و توصيل منتجات الجملة إلى موريتانيا'

env = Environment(
    loader=FileSystemLoader('src/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
