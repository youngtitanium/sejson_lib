from json import loads, dumps
import os
from random import randint
import logging

class sejson:
    """
    Этот класс позволяет легко редактировать json файлы.
    """

    
    def __init__(self, filename, rewrite=False, rw=False):
        """
        filename - путь к файлу.
        rewrite - если такой файл уже существует то заменить ли его?
        rw - если такой файл уже существует, но его
        содержимое не является json заменить его?
        Записать имя и путь к файлу.
        """
        path, filename = os.path.split(filename)
        if path=='':
            dir_list = os.listdir()
        else:
            dir_list = os.listdir(path)
        rx=False
        if filename in dir_list:
            logging.info('Найден файл с таким же именем.')
            if rewrite:
                with open(filename, 'w') as file:
                    file.write('{}')
                logging.info('Перезапись файла')
            else:
                filename = path+filename
                with open(filename) as file:
                    content = file.read()
                try:
                    loads(content)
                    logging.info('Файл успешно инициирован.')
                except Exception as e:
                    logging.info('Файл не в json формате.')
                    if rw:
                        with open(filename, 'w') as file:
                            file.write('{}')
                        logging.info('Файл перезаписан.')
                    else:
                        name, form =  '.'.join(filename.split('.')[0:-1]), filename.split('.')[-1]
                        while filename in dir_list:
                            filename=name+f'{randint(0, 2020)}.'+form
                        with open(filename, 'w') as file:
                            file.write('{}')
                        self.filename=filename
                        logging.info('Создан файл под именем: {}'.format(filename), filename)
        else:
            with open(filename, 'w') as file:
                file.write('{\n}')
            logging.info('Файл создан.')
        self.filename = filename

    @property
    def content(self):
        self.__content = self.dict_to_json(self.read())
        return self.read()

    @content.setter
    def content(self, value):
        if not isinstance(value, (dict, list, tuple)):
            raise TypeError('Incorrect content type!')
        jsoned = dumps(value, indent=4, ensure_ascii=False)
        self.__content = jsoned
        self.write(value)

    
    def read(self):
        """
        Прочитать содержимое файла.
        """
        with open(self.filename) as file:
            file_content = file.read()
            self.__content=dumps(loads(file_content), ensure_ascii=False, indent=4)
            return loads(file_content)

        
    def write(self, value: (dict, list, tuple)):
        """
        Заменить содержимое файла.
        """
        if not isinstance(value, (dict, list, tuple)):
            raise TypeError('Невозможно превратить {} в JSON'.format(type(value)))
        with open(self.filename, 'w') as file:
            file.write(dumps(value, ensure_ascii=False))
        return True

    def append(self, element: all, rw=True):
        """
        Если содержимое файла это список то внести определённый элемент в него.
        """
        content = self.read()
        if isinstance(content, list):
            content.append(element)
            self.write(content)
        else:
            if len(content)<1:
                if rw:
                    self.write([element])
                    return True
            raise Exception('Содержимое файла не является списком!')
    
    def update(self, key: str, value: all):
        """
        Эта функция позволяет заменить один элемент json.
        key - ключ по которому нужно заменить значение.
        value - новое значение.
        """
        if not isinstance(key, str):
            raise TypeError('Ключ должен быть строкой!')
        dct = self.read()
        dct[key]=value
        self.write(dct)
        return True


    def exists(self, key: str):
        """
        Проверить существует ли ключ в json.
        """
        if not isinstance(key, str):
            raise TypeError('Ключ должен быть строкой!')
        dct = self.read()
        if key in dct:
            return True
        else:
            return False

    def eqc(self, key: str, value: all):
        """
        Проверяет есть ли такой ключ в json и равно ли его значение указаному.
        """
        if not isinstance(key, str):
            raise TypeError('Ключ должен быть строкой!')
        
        if self.exists(key):
            if self.read()[key] == value:
                return True
        return False
        
    
    def __eq__(self, other):
        if other.__class__.__name__ == 'sejson':
            return self.read() == other.read()
        else:
            return False
        
        
    def updatemany(self, dct: dict):
        """
        Эта функция позволяет заменять несколько элементов в json.
        {Key: Value} где Key = ключ по которому нужно заменить значение
        и Value новое значение.
        Так же можно и добавить значение.
        """
        if not isinstance(dct, dict):
            raise TypeError('Аргумент dct должен быть словарём!')
        last_dct = self.read()
        for k, v in dct.items():
            last_dct[str(k)] = v
        self.write(last_dct)
        return True

    
    def beauty(self, infile: bool=True):
        """
        Превратить содержимое файла в более читабельное.
        Если infile=False то выведёт содержимое файла в красивом виде.
        """
        dct = self.read()
        if infile:
            with open(self.filename, 'w') as file:
                file.write(dumps(dct, ensure_ascii=False, indent=4))
            return True
        else:
            return dumps(dct, ensure_ascii=False, indent=4)

    def get(self, column: str):
        """
        Возвращает значение столбца если он есть.
        """
        if self.exists(column):
            return self.read()[column]
        else:
            return None
    @staticmethod
    def dict_to_json(raw_dict: dict):
        """
        Превращает python-словарь в json-строку.
        """
        if not isinstance(raw_dict, dict):
            raise TypeError('Значение raw_dict должно быть словарём!')
        return dumps(raw_dict, ensure_ascii=False, indent=4)

    @staticmethod
    def json_to_dict(raw_json: str):
        """
        Превращает json-строку в python-словарь.
        """
        if not isinstance(raw_json, str):
            raise TypeError('Значение raw_json должно быть строкой!')

        return loads(raw_json)
