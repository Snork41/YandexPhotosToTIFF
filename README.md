# test_Mycego
Тестовое задание

Скрипт собирает фото из папок (на Яндекс диске) в один tiff файл.
### Запуск скрипта:
- Cоздать виртуальное окружение (требуется версия Python 3.11 или больше):
    ```
    python -m venv venv
    ```
- Активировать виртуальное окружение:
    - macOS\Linux
        ```
        source venv/bin/activate
        ```
    - Windows
        ```
        venv\Scripts\activate
        ```
- Установить зависимости из файла __requirements.txt__ :
    ```
    pip install -r requirements.txt
    ```
- В переменной __required_dirs__ (файл test_Mycego.py) указать имена необходимых папок
- Запусть скрипт __test_Mycego.py__