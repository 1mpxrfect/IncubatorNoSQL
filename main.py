import os
import json


def create_table():
    table_name = input("Введите название таблицы: ")
    columns = []
    while True:
        column_name = input("Введите название столбца (нажми Enter, чтобы закончить): ")
        if not column_name:
            break
        column_type = input("Введите тип данных для столбца (int, float, str, bool): ")
        column = {"name": column_name, "type": column_type}
        columns.append(column)
    table = {"name": table_name, "columns": columns, "data": []}
    save_table(table)
    print(f"Таблица {table_name} успешно создана!")


def print_table(table, column_order=None):
    if not column_order:
        column_order = [column["name"] for column in table["columns"]]
    header = "\t".join(column_order)
    print(header)
    for row in table["data"]:
        values = [str(row.get(column_name, "")) for column_name in column_order]
        row_str = "\t".join(values)
        print(row_str)


def add_row():
    table_name = input("Введите название таблицы: ")
    table = read_data(table_name)
    if table:
        for column in table["columns"]:
            if column["name"] == "id":
                column["name"] = "id"
        index_column = None
        for column in table["columns"]:
            if column["name"] == "id":
                index_column = column
                table["columns"].remove(column)
                break
        if index_column:
            table["columns"].insert(0, index_column)
        else:
            table["columns"].insert(0, {"name": "id"})
        row = {}
        for column in table["columns"]:
            if column["name"] != "id":
                value = input(f"Введите значение для столбца {column['name']}: ")
                row[column['name']] = value
        row_index = len(table["data"])
        row["id"] = row_index + 1
        table["data"].append(row)
        save_table(table)
        print("Строка успешно добавлена!")
        print_table(table, ["id"] + [column["name"] for column in table["columns"] if column["name"] != "id"])
    else:
        print(f"Таблица {table_name} не найдена.")


def update_row():
    table_name = input("Введите название таблицы: ")
    table = read_data(table_name)
    if table:
        row_index = int(input("Введите номер строки, которую нужно обновить: ")) - 1
        if row_index >= len(table["data"]) or row_index < 0:
            print(f"Строка с индексом {row_index + 1} не найдена.")
        else:
            row = table["data"][row_index]
            for column in table["columns"]:
                value = input(f"Введите новое значение для столбца {column['name']} (старое значение: {row[column['name']]}): ")
                row[column['name']] = value
            save_table(table)
            print("Строка успешно обновлена!")
    else:
        print(f"Таблица {table_name} не найдена.")



def delete_row():
    table_name = input("Введите название таблицы: ")
    table = read_data(table_name)
    if table:
        row_index = int(input("Введите номер строки, которую нужно удалить: ")) - 1
        if row_index >= len(table["data"]) or row_index < 0:
            print(f"Строка с индексом {row_index + 1} не найдена.")
        else:
            table["data"].pop(row_index)
            save_table(table)
            print("Строка успешно удалена!")
    else:
        print(f"Таблица {table_name} не найдена.")

def read_data(table_name):
    filename = f"{table_name}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    else:
        return None


def save_table(table):
    filename = f"{table['name']}.json"

    with open(filename, "w") as f:
        json.dump(table, f, indent=4, ensure_ascii=False)


def sort_table():
    table_name = input("Введите название таблицы: ")
    table = read_data(table_name)
    if table:
        column_name = input("Введите название столбца для сортировки: ")
        sort_order = input("Введите порядок сортировки (asc/desc): ")
        if column_name in [column['name'] for column in table['columns']]:
            table['data'] = sorted(table['data'], key=lambda x: x[column_name], reverse=(sort_order.lower() == 'desc'))
            save_table(table)
            print("Таблица успешно отсортирована!")
        else:
            print(f"Столбец {column_name} не найден.")
    else:
        print(f"Таблица {table_name} не найдена.")


def filter_table():
    table_name = input("Введите название таблицы: ")
    table = read_data(table_name)
    if table:
        column_name = input("Введите название столбца для фильтрации: ")
        filter_value = input("Введите значение для фильтрации: ")
        if column_name in [column['name'] for column in table['columns']]:
            table['data'] = list(filter(lambda x: x[column_name] == filter_value, table['data']))
            save_table(table)
            print("Таблица успешно отфильтрована!")
        else:
            print(f"Столбец {column_name} не найден.")
    else:
        print(f"Таблица {table_name} не найдена.")


while True:
    print('\n\t========================================')
    print("\t* 1. Создать новую таблицу             *")
    print("\t* 2. Добавить строку в таблицу         *")
    print("\t* 3. Обновить строку в таблице         *")
    print("\t* 4. Удалить строку из таблицы         *")
    print("\t* 5. Вывести таблицу на экран          *")
    print("\t* 6. Отсортировать таблицу             *")
    print("\t* 7. Отфильтровать таблицу (Не советую)*")
    print("\t* 8. Выйти из программы                *")
    print('\t========================================')

    try:
        choice = int(input("\tВведите номер > : "))
        print('\t==========================================')

        if choice == 1:
            create_table()
        elif choice == 2:
            add_row()
        elif choice == 3:
            update_row()
        elif choice == 4:
            delete_row()
        elif choice == 5:
            table_name = input("Введите название таблицы: ")
            table = read_data(table_name)
            if table:
                print(f"Таблица '{table_name}':")
                for column in table["columns"]:
                    print(column['name'].ljust(15), end="")
                print()
                for row in table["data"]:
                    for column in table["columns"]:
                        print(str(row[column['name']]).ljust(15), end="")
                    print()
            else:
                print(f"Таблица {table_name} не найдена.")
        elif choice == 6:
            sort_table()
        elif choice == 7:
            filter_table()
        elif choice == 8:
            print("Гуд Бай!")
            break
        else:
            print("Не правильная команда, попробуйте еще раз.")

    except ValueError:
        print("\nВы ввели не число!")
