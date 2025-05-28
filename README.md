### Рекомендую открыть файл примера и скопировать шаблон оттуда. В шаблон передается `items`.


Пример вывода:

![image](https://github.com/user-attachments/assets/70a7a513-8f94-499f-ad11-08cc0a8199c7)

Listing Generator
============

Утилита для генерации листинга кода для курсовых работ и отчетов

Установка
------------
Для веб версии просто склонируйте репозиторий:

```bash
$ git clone https://github.com/rasputyashka/listing_generator.git
$ cd listing_generator
```

Для CLI версии склонируйте репозиторий и установите зависимости в венв

```bash
$ git clone https://github.com/rasputyashka/listing_generator.git
$ cd listing_generator
$ uv sync && . .venv/bin/activate
```

Ну или

```bash
$ git clone https://github.com/rasputyashka/listing_generator.git
$ cd listing_generator
$ python -m venv .venv && . .venv/bin/activate
$ pip install .
```

Использование
-----
WEB:
```bash
$ docker compose up
```
Веб версия доступна по адресу 127.0.0.1:5000

CLI:
```bash
$ genlist --help
usage: genlist [-h] -i I -d D [-iext IEXT [IEXT ...]] [-eext EEXT [EEXT ...]] [-iname INAME [INAME ...]]
               [-ename ENAME [ENAME ...]] -o O [-m]

options:
  -h, --help            show this help message and exit
  -i I                  path to template document
  -d D                  path to directory with files needed for listing
  -iext IEXT [IEXT ...]
                        list of included extensions
  -eext EEXT [EEXT ...]
                        list of excluded extensions
  -iname INAME [INAME ...]
                        list of included filenames
  -ename ENAME [ENAME ...]
                        list of excluded filenames
  -o O                  path to result .docx file (explicit extension is required)
  -m, --minimize        reduce amount of code by replacing doubled line breaks with one line break
```
пример использования:

```$ genlist -iext .py -ename __init__.py  -i examples/example.docx -m -d ~/code/djplathack/src/djplathack -o /tmp/file.docx```
