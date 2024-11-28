from database.database import Database, EmployeeTable, DepartmentTable, AddressTable


if __name__ == "__main__" :
    db = Database()

    # Создание таблиц в базе данных
    db.register_table("employees", EmployeeTable())
    db.register_table("departments", DepartmentTable())
    db.register_table("addresses", AddressTable())

    # Вставка элементов
    db.insert("addresses", "1,Москва,Тверская,10")
    db.insert("addresses", "2,Санкт-Петербург,Невский пр.,22")
    db.insert("addresses", "3,Новосибирск,Красный пр.,50")

    db.insert("departments", "1,Отдел продаж,1")
    db.insert("departments", "2,Маркетинг,2")
    db.insert("departments", "3,IT-отдел,3")

    db.insert("employees", "1,Alice,30,70000,1")
    db.insert("employees", "2,Bob,29,100000,1")
    db.insert("employees", "3,Ivan,28,55000,2")
    db.insert("employees", "4,Olga,25,45000,3")
    db.insert("employees", "5,Sergey,40,70000,2")
