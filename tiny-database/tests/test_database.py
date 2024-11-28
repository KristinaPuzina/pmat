import pytest
import os
import tempfile
from database.database import Database, EmployeeTable, DepartmentTable, AddressTable

@pytest.fixture
def temp_employee_file():
    """ Создаем временный файл для таблицы рабочих """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def temp_department_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    yield temp_file.name
    os.remove(temp_file.name)

@pytest.fixture
def temp_address_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    yield temp_file.name
    os.remove(temp_file.name)

#Пример, как используются фикстуры
@pytest.fixture
def database(temp_employee_file, temp_department_file, temp_address_file):
    """ Данная фикстура задает БД и определяет таблицы. """
    db = Database()

    # Используем временные файлы для тестирования файлового ввода-вывода в EmployeeTable и DepartmentTable
    employee_table = EmployeeTable()
    employee_table.FILE_PATH = temp_employee_file
    department_table = DepartmentTable()
    department_table.FILE_PATH = temp_department_file
    address_table = AddressTable()
    address_table.FILE_PATH = temp_address_file

    db.register_table("employees", employee_table)
    db.register_table("departments", department_table)
    db.register_table("addresses", address_table)

    return db

def test_insert_employee(database):
    database.insert("employees", "1,Alice,30,70000,1")
    database.insert("employees", "2,Bob,28,60000,1")

    # Проверяем вставку, подгружая с CSV
    employee_data = database.select("employees", 1, 2)
    print(employee_data)
    assert len(employee_data) == 2
    assert employee_data[0] == {'employee_id': '1', 'name': 'Alice', 'age': '30', 'salary': '70000', 'department_id': '1'}
    assert employee_data[1] == {'employee_id': '2', 'name': 'Bob', 'age': '28', 'salary': '60000', 'department_id': '1'}

    with pytest.raises(ValueError):
        database.insert("employees", "2,John,30,47000,1")


def test_insert_department(database):
    database.insert("departments", "1,Отдел продаж,1")
    data = database.select("departments", "Отдел продаж")
    assert data[0] == {'department_id': '1', 'department_name': 'Отдел продаж', 'address_id': '1'}

    with pytest.raises(ValueError):
        database.insert("departments", "1,Маркетинг")


def test_join_employees_departments(database):
    database.insert("employees", "1,Alice,30,70000,1")
    database.insert("employees", "2,Bob,28,60000,1")
    database.insert("departments", "1,Отдел продаж,1")

    data = database.join(["employees", "departments"], ["department_id"])
    assert data == [
        {
            'employee_id': '1', 'name': 'Alice',
            'age': '30', 'salary': '70000',
            'department_id': '1', 'department_name': 'Отдел продаж',
            'address_id': '1'
        },
        {
            'employee_id': '2', 'name': 'Bob',
            'age': '28', 'salary': '60000',
            'department_id': '1', 'department_name': 'Отдел продаж',
            'address_id': '1'
        }
    ]

def test_select_employee(database):
    database.insert("employees", "1,Alice,30,70000,1")
    database.insert("employees", "2,Bob,28,60000,1")

    employee_data = database.select("employees", 1, 2)
    assert len(employee_data) == 2
    assert employee_data[0] == {'employee_id': '1', 'name': 'Alice', 'age': '30', 'salary': '70000', 'department_id': '1'}
    assert employee_data[1] == {'employee_id': '2', 'name': 'Bob', 'age': '28', 'salary': '60000', 'department_id': '1'}

    employee_data = database.select("employees", 1, 1)
    assert employee_data[0] == {'employee_id': '1', 'name': 'Alice', 'age': '30', 'salary': '70000', 'department_id': '1'}

    employee_data = database.select("employees", 2, 2)
    assert employee_data[0] == {'employee_id': '2', 'name': 'Bob', 'age': '28', 'salary': '60000', 'department_id': '1'}

    employee_data = database.select("employees", 3, 4)
    assert len(employee_data) == 0

def test_insert_address(database):
    database.insert("addresses", "1,Москва,Тверская,10")
    data = database.select("addresses", 1, 1)
    assert data[0] == {'address_id': '1', 'city': 'Москва', 'street': 'Тверская', 'house_number': '10'}

    with pytest.raises(ValueError):
        database.insert("addresses", "1,Санкт-Петербург,Невский пр.,22")

def test_select_address(database):
    database.insert("addresses", "1,Москва,Тверская,10")
    database.insert("addresses", "2,Санкт-Петербург,Невский пр.,22")

    address_data = database.select("addresses", 1, 2)
    assert len(address_data) == 2

    assert address_data[0] == {'address_id': '1', 'city': 'Москва', 'street': 'Тверская', 'house_number': '10'}
    assert address_data[1] == {'address_id': '2', 'city': 'Санкт-Петербург', 'street': 'Невский пр.', 'house_number': '22'}

    address_data = database.select("addresses", 1, 1)
    assert address_data[0] == {'address_id': '1', 'city': 'Москва', 'street': 'Тверская', 'house_number': '10'}

    address_data = database.select("addresses", 2, 2)
    assert address_data[0] == {'address_id': '2', 'city': 'Санкт-Петербург', 'street': 'Невский пр.', 'house_number': '22'}

    address_data = database.select("addresses", 3, 4)
    assert len(address_data) == 0

def test_join_employees_departments_addresses(database):
    database.insert("addresses", "1,Москва,Тверская,10")
    database.insert("addresses", "2,Санкт-Петербург,Невский пр.,22")
    database.insert("departments", "1,Отдел продаж,1")
    database.insert("departments", "2,Маркетинг,2")
    database.insert("employees", "1,Alice,30,70000,1")
    database.insert("employees", "2,Bob,29,100000,1")
    database.insert("employees", "3,Ivan,28,55000,2")

    data = database.join(["employees", "departments", "addresses"], ["department_id", "address_id"])

    assert data == [
        {
            'employee_id': '1', 'name': 'Alice',
            'age': '30', 'salary': '70000', 'department_id': '1',
            'department_name': 'Отдел продаж', 'address_id': '1',
            'city': 'Москва', 'street': 'Тверская', 'house_number': '10'
        },
        {
            'employee_id': '2', 'name': 'Bob',
            'age': '29', 'salary': '100000', 'department_id': '1',
            'department_name': 'Отдел продаж', 'address_id': '1',
            'city': 'Москва', 'street': 'Тверская', 'house_number': '10'
        },
        {
            'employee_id': '3', 'name': 'Ivan',
            'age': '28', 'salary': '55000', 'department_id': '2',
            'department_name': 'Маркетинг', 'address_id': '2',
            'city': 'Санкт-Петербург', 'street': 'Невский пр.', 'house_number': '22'
        }
    ]

def test_aggregate_employees(database):
    database.insert("employees", "1,Alice,30,70000,1")
    database.insert("employees", "2,Bob,29,100000,1")
    database.insert("employees", "3,Ivan,28,55000,2")
    database.insert("employees", "4,Olga,25,45000,3")
    database.insert("employees", "5,Sergey,40,70000,2")

    res = database.aggregate("employees", "employee_id", len)
    assert res == 5

    res = database.aggregate("employees", "salary", min)
    assert res == 45000

    res = database.aggregate("employees", "salary", max)
    assert res == 100000

    res = database.aggregate("employees", "salary", lambda x: sum(x) / len(x))
    assert res == 68000.0
