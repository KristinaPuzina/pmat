from abc import ABC, abstractmethod
import csv
import os


class SingletonMeta(type):
    """ Синглтон метакласс для Database. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """ Класс-синглтон базы данных с таблицами, хранящимися в файлах. """

    def __init__(self):
        self.tables = {}

    def register_table(self, table_name, table):
        self.tables[table_name] = table

    def insert(self, table_name, data):
        table = self.tables.get(table_name)
        if table:
            table.insert(data)
        else:
            raise ValueError(f"Table {table_name} does not exist.")

    def select(self, table_name, *args):
        table = self.tables.get(table_name)
        return table.select(*args) if table else None

    def join(self, table_names, join_attrs):
        tables = [self.tables.get(table_name) for table_name in table_names]

        if tables.count(None):
            index = tables.index(None)
            raise ValueError(f"Table {table_names[index]} does not exist.")

        joined_data = self.__join_two_tables(tables[0].data, tables[1].data, join_attrs[0])

        for i in range(2, len(tables)):
            joined_data = self.__join_two_tables(joined_data, tables[i].data, join_attrs[i - 1])

        return joined_data

    @staticmethod
    def __join_two_tables(data1, data2, key):
        joined_data = []

        for row1 in data1:
            for row2 in data2:
                if row1.get(key, None) == row2.get(key, None) is not None:
                    joined_data.append({**row1, **row2})

        return joined_data

    def aggregate(self, table_name, column, func):
        table = self.tables.get(table_name)

        if not table:
            raise ValueError(f"Table {table_name} does not exist.")

        if column not in table.ATTRS:
            raise ValueError(f"There is no such {column} column in the table {table_name}")

        values = [int(row[column]) for row in table.data]

        return func(values)


class Table(ABC):
    """ Абстрактный базовый класс для таблиц с вводом/выводом файлов CSV. """

    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def select(self, *args):
        pass


class EmployeeTable(Table):
    """ Таблица сотрудников с методами ввода-вывода из файла CSV. """
    ATTRS = ('employee_id', 'name', 'age', 'salary', 'department_id')
    FILE_PATH = 'employee_table.csv'

    def __init__(self):
        self.data = []
        self.load()  # Подгружаем из CSV-файла сразу при инициализации

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split(',')))

        for row in self.data:
            if (row["employee_id"], row["department_id"]) == (entry["employee_id"], entry["department_id"]):
                raise ValueError("The pair (employee_id, department_id) must be unique")

        self.data.append(entry)
        self.save()

    def select(self, start_id, end_id):
        return [entry for entry in self.data if start_id <= int(entry['employee_id']) <= end_id]

    def save(self):
        with open(self.FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []


class DepartmentTable(Table):
    """ Таблица подразделенией с вводлм-выводом в/из CSV файла. """
    ATTRS = ('department_id', 'department_name', 'address_id')
    FILE_PATH = 'department_table.csv'

    def __init__(self):
        self.data = []
        self.load()

    def select(self, department_name):
        return [entry for entry in self.data if department_name == entry['department_name']]

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split(',')))

        for row in self.data:
            if row["department_id"] == entry["department_id"]:
                raise ValueError("department_id must be unique")

        self.data.append(entry)
        self.save()

    def save(self):
        with open(self.FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []


class AddressTable(Table):
    """ Таблица адресов с вводом-выводом в/из CSV файла. """
    ATTRS = ('address_id', 'city', 'street', 'house_number')
    FILE_PATH = 'address_table.csv'

    def __init__(self):
        self.data = []
        self.load()

    def select(self, start_id, end_id):
        return [entry for entry in self.data if start_id <= int(entry['address_id']) <= end_id]

    def insert(self, data):
        entry = dict(zip(self.ATTRS, data.split(',')))

        for row in self.data:
            if row["address_id"] == entry["address_id"]:
                raise ValueError("address_id must be unique")

        self.data.append(entry)
        self.save()

    def save(self):
        with open(self.FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.ATTRS)
            writer.writeheader()
            writer.writerows(self.data)

    def load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as f:
                reader = csv.DictReader(f)
                self.data = [row for row in reader]
        else:
            self.data = []
