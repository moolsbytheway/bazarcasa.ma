from jinja2 import Environment, FileSystemLoader, select_autoescape

output_folder = "output"
product_files_path = "products/current.csv"

CBM_PRICE = 50000
DEFAULT_PAGE_TITLE = 'بازار كازا - توفير و توصيل منتجات الجملة إلى موريتانيا'

env = Environment(
    loader=FileSystemLoader('src/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
=CNUM(GAUCHE(I2, TROUVE("x", I2) - 1)) * CNUM(STXT(I2, TROUVE("x", I2) + 1, TROUVE("x", I2, TROUVE("x", I2) + 1) - TROUVE("x", I2) - 1)) * CNUM(DROITE(I2, LONGUEUR(I2) - TROUVE("x", I2, TROUVE("x", I2) + 1)))
