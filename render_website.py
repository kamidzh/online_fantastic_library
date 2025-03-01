import argparse
import json
import os

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Проект создан для скачивания книг с сайта tululu.org'
    )
    parser.add_argument('--dest_folder', help='dest_folder', default='media')
    parser.add_argument('--parameters_file', help='parameters_file', default='parameters.json')
    args = parser.parse_args()
    return args


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open(args.parameters_file, 'r', encoding='utf-8') as my_file:
        books_parameters = json.load(my_file)
    os.makedirs('pages', exist_ok=True)
    books_in_page = 10
    book_groups = list(chunked(books_parameters, books_in_page))
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