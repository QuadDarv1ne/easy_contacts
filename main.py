import json
import os
import re

CONTACTS_FILE = 'contacts.json'


def load_contacts():
    """Загружает контакты из файла JSON, если файл существует и данные корректны."""
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
            try:
                contacts = json.load(file)
                if isinstance(contacts, list):
                    # Проверяем, что каждый элемент списка — это словарь
                    if all(isinstance(contact, dict) for contact in contacts):
                        return contacts
                    else:
                        print("Ошибка: Неверная структура данных в файле.")
                        return []
                else:
                    print("Ошибка: Ожидался список контактов, но найден другой тип данных.")
                    return []
            except json.JSONDecodeError:
                print("Ошибка: Невозможно прочитать JSON файл. Возможно, файл поврежден.")
                return []
    return []


def save_contacts(contacts):
    """Сохраняет контакты в файл JSON."""
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)


def is_valid_phone(phone):
    """Проверяет формат номера телефона (например, 123-456-7890)."""
    return re.match(r'^\d{3}-\d{3}-\d{4}$', phone)


def is_valid_email(email):
    """Проверяет формат электронной почты."""
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email)


def input_with_validation(prompt, validation_fn, error_message):
    """Запрашивает ввод у пользователя с проверкой."""
    while True:
        value = input(prompt)
        if validation_fn(value):
            return value
        print(error_message)


def add_contact(contacts):
    """Добавляет новый контакт с проверкой валидности данных."""
    name = input("Введите имя: ").strip()
    surname = input("Введите фамилию: ").strip()
    phone = input_with_validation("Введите номер телефона (например, 123-456-7890): ", is_valid_phone, "Некорректный формат телефона.")
    email = input_with_validation("Введите электронную почту: ", is_valid_email, "Некорректный формат электронной почты.")

    # Проверка на дублирование контакта
    if any(contact['name'] == name and contact['surname'] == surname for contact in contacts):
        print("Контакт с таким именем и фамилией уже существует.")
        return

    contact = {
        "name": name,
        "surname": surname,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Контакт успешно добавлен.")


def remove_contact(contacts):
    """Удаляет контакт по имени и фамилии."""
    name = input("Введите имя для удаления: ").strip()
    surname = input("Введите фамилию для удаления: ").strip()

    for contact in contacts:
        if contact['name'] == name and contact['surname'] == surname:
            contacts.remove(contact)
            save_contacts(contacts)
            print(f"Контакт {name} {surname} удален.")
            return

    print(f"Контакт {name} {surname} не найден.")


def view_contacts(contacts):
    """Просматривает все контакты."""
    if contacts:
        print("Список контактов:")
        for contact in contacts:
            if isinstance(contact, dict):  # Проверяем, что каждый контакт — это словарь
                print(f"- {contact.get('name', 'Не указано')} {contact.get('surname', 'Не указано')}, {contact.get('phone', 'Не указано')}, {contact.get('email', 'Не указано')}")
            else:
                print("Ошибка: Один из контактов имеет неверную структуру.")
    else:
        print("Контакты отсутствуют.")


def search_contact(contacts):
    """Поиск контактов по имени или фамилии."""
    search_term = input("Введите имя или фамилию для поиска: ").strip().lower()

    results = [contact for contact in contacts if search_term in contact['name'].lower() or search_term in contact['surname'].lower()]

    if results:
        print("Найденные контакты:")
        for contact in results:
            print(f"- {contact['name']} {contact['surname']}, {contact['phone']}, {contact['email']}")
    else:
        print(f"Контакты, соответствующие запросу '{search_term}', не найдены.")


def main():
    contacts = load_contacts()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить контакт")
        print("2. Удалить контакт")
        print("3. Просмотреть контакты")
        print("4. Поиск контакта")
        print("5. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            remove_contact(contacts)
        elif choice == '3':
            view_contacts(contacts)
        elif choice == '4':
            search_contact(contacts)
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()


'''
Описание программы:
    1. Загрузка и сохранение контактов: Используются функции `load_contacts` и `save_contacts` для работы с файлом `contacts.json`.
    2. Добавление контакта: Функция `add_contact` запрашивает данные у пользователя и добавляет новый контакт.
    3. Удаление контакта: Функция `remove_contact` позволяет удалить контакт по имени и фамилии.
    4. Просмотр контактов: Функция `view_contacts` выводит список всех контактов.
    5. Главная функция: В main реализован цикл, который позволяет пользователю выбирать действия.

Примечание:
    Не забудьте создать файл `contacts.json`, чтобы программа могла сохранить данные.
'''

# TODO: Заметки
## Преподаватель: Дуплей Максим Игоревич
## Дата: 26.09.2024
