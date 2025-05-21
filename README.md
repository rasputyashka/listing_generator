## приложение для генерации листинга кода для курсовых работ и отчетов

```
genlist --help                                                                                                                  
usage: genlist [-h] -i I -d D [-iext IEXT [IEXT ...]] [-eext EEXT [EEXT ...]] [-iname INAME [INAME ...]] [-ename ENAME [ENAME ...]] -o O

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
```

### пример использования

```$ genlist -iext .py -ename __init__.py  -i examples/example.docx  -d ~/code/djplathack/src/djplathack -o /tmp/file.docx```

Пример вывода:

![image](https://github.com/user-attachments/assets/70a7a513-8f94-499f-ad11-08cc0a8199c7)
