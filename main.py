from datetime import datetime
import json

def add_income():
    global balance, operations
    amount = int(input('Сумма дохода:'))
    print('Выберите категорию дохода:')
    for i, cat in enumerate(income_categories, 1):
        print(f'{i}. {cat}')
    print(f"{len(income_categories) + 1}. Другая (ввести вручную)")

    cat_choice = int(input('Ваш выбор:'))

    if 1 <= cat_choice <= len(income_categories):
        category = income_categories[cat_choice - 1]
    else:
        category = input('Введите название категории:')

    operations.append({
        'type': 'доход',
        'amount': amount,
        'category': category,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M')
    })
    balance += amount
    print(f'Добавлен доход: {amount} руб.')
    save_operations()

def add_expense():
    global balance, operations
    amount = int(input('Сумма расхода:'))
    print('Выберите категорию расхода:')
    for i, cat in enumerate(expense_categories, 1):
        print(f'{i}. {cat}')
    print(f"{len(expense_categories) + 1}. Другая (ввести вручную)")

    cat_choice = int(input('Ваш выбор:'))

    if 1 <= cat_choice <= len(expense_categories):
        category = expense_categories[cat_choice - 1]
    else:
        category = input('Введите название категории:')

    operations.append({
        'type': 'расход',
        'amount': amount,
        'category': category,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M')
    })
    balance -= amount
    print(f'Добавлен расход: {amount} руб.')
    save_operations()

def history_operations():
    print('\n====== ИСТОРИЯ ОПЕРАЦИЙ =======')

    if not operations:
        print('История пуста.')
    else:

        for operation in operations:
            print(f"{operation['date']} | {operation['type']:6} | {operation['category']:10}"
                  f" | {operation['amount']:>8} руб.")
        print('===========\n')


def edit_operations():
    global operations, balance
    print('Редактирование операции')
    while True:
        if not show_operations_with_number():
            continue
        try:
            op_num = int(input('Введите номер операции для редактирования: '))
            if 1 <= op_num <= len(operations):
                op = operations[op_num - 1]
                old_amount = op['amount']
                old_type = op['type']
                print(f"\nТекущая операция: {op['date']} | {op['type']} | {op['category']} | {op['amount']} руб.")
                print('Что редактируем? ')
                print('1. Сумму')
                print('2. Категорию')
                print('3. Всё')
                edit_choice = int(input('Ваш выбор:'))

                if op['type'] == 'доход':
                    balance -= op['amount']
                else:
                    balance += op['amount']

                if edit_choice in [1, 3]:
                    new_amount = int(input('Новая сумма: '))
                    op['amount'] = new_amount

                    if op['type'] == 'доход':
                        balance += new_amount
                    else:
                        balance -= new_amount

                if edit_choice in [2, 3]:
                    print('Выберите новую категорию: ')
                    if op['type'] == 'доход':
                        categories = income_categories
                    else:
                        categories = expense_categories

                    for i, cat in enumerate(categories, 1):
                        print(f'{i}. {cat}')
                    print(f'{len(categories) + 1}. ✏️ Другая (ввести вручную)')
                    try:
                        cat_choice = int(input('Ваш выбор: '))
                    except ValueError:
                        print('Введите число!')
                    if 1 <= cat_choice <= len(categories):
                        op['category'] = categories[cat_choice - 1]
                    else:
                        op['category'] = input('Введите название категории: ')

                op['date'] = datetime.now().strftime('%d.%m.%Y %H:%M')

                save_operations()
                print('Операция успешно отредактирована!')
                break
            else:
                print('Неверный номер операции!')
        except ValueError:
            print('Пожалуйста, введите число!')

def del_operations():
    global operations, balance
    print('Удаление операции')
    while True:
        if not show_operations_with_number():
            continue
        try:
            op_num = int(input('Введите номер операции для удаления: '))
            if 1 <= op_num <= len(operations):
                op = operations[op_num - 1]
                print('Операция для удаления: ')
                print(f"{op['date']} | {op['type']} | {op['category']} | {op['amount']} руб.")

                confirm = input('Подтвердить удаление? (да/нет)')
                if confirm.lower() == 'да':
                    if op['type'] == 'доход':
                        balance -= op['amount']
                    else:
                        balance += op['amount']
                    del operations[op_num - 1]
                    save_operations()
                    print('Операция удалена!')
                else:
                    print('Удаление отменено!')
            else:
                print('Номер операции неверный!')
        except ValueError:
            print('Пожалуйста, введите число!')

def save_operations():
    global operations, balance
    with open('finance_data.json', 'w', encoding='utf-8') as file:
        json.dump({
            'operations': operations,
            'balance': balance,
        }, file, ensure_ascii=False, indent=2)
        print('Данные сохранены!')

def load_operations():
    global operations, balance
    try:
        with open('finance_data.json', encoding='utf-8') as file:
            data = json.load(file)
            operations = data['operations']
            balance = data['balance']
            print(f'Загружено {len(operations)} операций.')
            print(f'Текущий баланс: {balance} руб.')
    except FileNotFoundError:
        print('Файл с данными не найден. Начинаем с нуля.')
        operations = []
        balance = 0
    except json.JSONDecodeError:
        print('Ошибка чтения файла. Создаем новый.')
        operations = []
        balance = 0

def show_operations_with_number():
    if not operations:
        print('История пуста')
        return False
    for i, op in enumerate(operations, 1):
        amount = op['amount']
        if op['type'] == 'доход':
            amount_str = f"+{amount:>8,.0f}".replace(',', '')
        else:
            amount_str = f"-{amount:>8,.0f}".replace(',', '')
        print(f"{i:<4} {op['date']:<16} {op['type']:<8} {op['category']:<15} {amount_str} руб.")
    return True


def show_statistics():
    global operations
    total_income = 0
    total_expense = 0
    expense_by_category = {}

    for op in operations:
        if op['type'] == 'доход':
            total_income += op['amount']
        else:
            total_expense += op['amount']
            cat = op['category']
            if cat in expense_by_category:
                expense_by_category[cat] += op['amount']
            else:
                expense_by_category[cat] = op['amount']


    print('\n' + '=' * 40)
    print('СТАТИСТИКА')
    print('=' * 40)
    print(f'Доходы: {total_income} руб.')
    print(f'Расходы: {total_expense} руб.')
    print(f'Баланс: {total_income - total_expense} руб.')

    if expense_by_category:
        print('\nТоп категорий расходов:')
        sorted_cats = sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)[:3]
        for cat, amount in sorted_cats:
            print(f'{cat}: {amount} руб.')



income_categories = ['Зарплата', 'Кэшбэк', 'Приятные находки', 'Прочие доходы']
expense_categories = ['Еда', 'Транспорт', 'Тренировки', 'Прочие расходы']
operations = []
balance = 0
load_operations()

while True:
    print('\nФинансовый трекер')
    print(f'Баланс - {balance} руб.')
    print('\n1. Добавить доход')
    print('2. Добавить расход')
    print('3. Показать историю')
    print('4. Редактировать операцию')
    print('5. Удалить операцию')
    print('6. Статистика')
    print('7. Выход')

    try:
        choice = int(input('\nВыберите действие:'))

        if choice == 1:
            add_income()

        elif choice == 2:
            add_expense()

        elif choice == 3:
            history_operations()

        elif choice == 4:
            edit_operations()

        elif choice == 5:
            del_operations()

        elif choice == 6:
            show_statistics()

        elif choice == 7:
            print('До свидания!')
            break
        else:
            print('Пожалуйста, введите число 1-4')
    except ValueError:
        print('Некорректный выбор! Пожалуйста, введите число!')