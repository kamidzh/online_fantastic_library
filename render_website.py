from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import argparse
from more_itertools import chunked
import os


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Проект создан для скачивания книг с сайта tululu.org'
    )
    parser.add_argument('--dest_folder', help='dest_folder', default='results')
    args = parser.parse_args()
    return args


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open(f"{args.dest_folder}/parameters.json", "r", encoding='utf-8') as my_file:
        file_contents = my_file.read()
    os.makedirs('pages', exist_ok=True)
    books_parameters = json.loads(file_contents)
    book_groups = list(chunked(books_parameters, 10))
    pages_amount = len(book_groups)
    for num, book_group in enumerate(book_groups):
        rendered_page = template.render(
            books = book_group,
            books_folder = f'{args.dest_folder}/books',
            images_folder = f'{args.dest_folder}/images',
            pages_amount = pages_amount,
            my_page = num + 1
        )
        with open(f'pages/index{num + 1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    print('Site rebuilt')


if __name__ == '__main__':
    args = get_arguments()
    rebuild()
    server = Server()
    server.watch('template.html', rebuild)
    server.serve(root='.')