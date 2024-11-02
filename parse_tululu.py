import requests
import os
from bs4 import BeautifulSoup	
from pathvalidate import sanitize_filename
import pathlib
from urllib.parse import urljoin, urlsplit, unquote
import argparse
from time import sleep
import json


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(response, filename, folder):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_image(url, filename, folder):
    response = requests.get(url)
    response.raise_for_status()
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(folder, filename)
    with open(unquote(file_path), 'wb') as file:
        file.write(response.content)


def parse_book_page(soup, url):
    book_name = soup.select_one('h1').text.split('::')
    title = book_name[0].strip()
    author = book_name[1].strip()
    genres = soup.select('span.d_book a')
    genres = [genre.text for genre in genres]
    comments = soup.select('div.texts span.black')
    comments_text = [comment.text for comment in comments]
    image = soup.select_one('div.bookimage img')['src']
    image_url = urljoin(url, image)
    book_parameters = {
        "author": author,
        "title": title,
        "genres": genres,
        "comments": comments_text,
        "image_url": image_url,
    }
    return book_parameters


def get_category_books_url(start_page, end_page):
    book_links = []
    for page in range(start_page, end_page):
        url = f'https://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.select('table.d_book')
        for book in books:
            book_url = urljoin(url, book.select_one('a')['href'])
            book_links.append(book_url)
    return book_links


def main():
    parser = argparse.ArgumentParser(
        description='Проект создан для скачивания книг с сайта tululu.org'
    )
    parser.add_argument('--start_page', help='start_page', default=1, type=int)
    parser.add_argument('--end_page', help='end_page', default=701, type=int)
    parser.add_argument('--skip_imgs', help='skip images', action='store_true')
    parser.add_argument('--skip_txt', help='skip txt', action='store_true')
    parser.add_argument('--dest_folder', help='dest_folder', default='results')
    args = parser.parse_args()
    all_parameters = []
    for url in get_category_books_url(args.start_page, args.end_page):
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            parameters = parse_book_page(soup, url)
            all_parameters.append(parameters)
            if not args.skip_imgs:
                image_url = parameters['image_url']
                filename = urlsplit(image_url).path.split('/')[-1]
                img_folder = f'{args.dest_folder}/images/'
                download_image(image_url, filename, img_folder)
            if not args.skip_txt:
                number = urlsplit(url).path.split('/')[-2][1:]
                payload = {'id' : number}
                download_url = 'https://tululu.org/txt.php'
                download_response = requests.get(download_url, params=payload)
                download_response.raise_for_status()
                check_for_redirect(download_response)
                book_title = parameters['title']
                book_folder = f'{args.dest_folder}/books/'
                download_txt(download_response, book_title, book_folder)
        except requests.exceptions.HTTPError:
            print('такой книги нет')
        except requests.exceptions.ConnectionError:
            print('Попытка подключения к серверу')
            sleep(20)
    pathlib.Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
    with open(f"{args.dest_folder}/parameters.json", "w", encoding='utf8') as file:
        json.dump(all_parameters, file, ensure_ascii=False)


if __name__ == '__main__':
    main()