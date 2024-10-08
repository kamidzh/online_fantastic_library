# Парсер книг с сайта tululu.org

## Описание

Проект создан для скачивания книг с сайта [tululu.org](https:/tululu.org/).

## Как установить

Для запуска скрипта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 

```
pip install -r requirements.txt
```

## Запуск

Для запуска скрипта используйте следующую команду в консоли:

```
python parse_tululu.py
```

Для программы доступны параметры:

`--start_page` — номер стартовой страницы, по умолчанию - 1

`--end_page` — номер последней страницы, по умолчанию - 701

`--dest_folder` — путь к каталогу с результатами парсинга: картинкам, книгам, JSON, по умолчанию - папка results

`--skip_imgs` — не скачивать картинки

`--skip_txt` — не скачивать книги

Примеры запуска скрипта:

```
$ python parse_tululu.py --start_page 700 --end_page 701 --dest_folder folder_name --skip_imgs --skip_txt

```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).