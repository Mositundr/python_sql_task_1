import psycopg2
import os
import time

# Жду запуска базы
time.sleep(5)

# Подключаюсь к базе
db_url = os.getenv("DATABASE_URL")
try:
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    # Очищаю таблицу перед началом
    cursor.execute("DROP TABLE IF EXISTS employees")
    
    # 1. Создаю таблицу
    cursor.execute("""
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            position VARCHAR(100),
            salary INTEGER
        )
    """)
    print("Таблица employees создана")

    # 2. Добавляю 5 сотрудников по заданию
    employees = [
        ("Иван", "Разработчик", 45000),
        ("Анна", "Менеджер", 55000),
        ("Пётр", "Аналитик", 60000),
        ("Мария", "Дизайнер", 48000),
        ("Сергей", "Тестировщик", 52000)
    ]
    cursor.executemany("INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)", employees)
    conn.commit()
    print("Добавлено 5 сотрудников")

    # Показываю исходную таблицу
    cursor.execute("SELECT name, position, salary FROM employees")
    all_employees = cursor.fetchall()
    print("Исходная таблица сотрудников:")
    for employee in all_employees:
        print(f"Имя: {employee[0]}, Должность: {employee[1]}, Зарплата: {employee[2]}")

    # 4. Обновляю зарплату Ивана
    cursor.execute("UPDATE employees SET salary = 60000 WHERE name = 'Иван'")
    conn.commit()
    print("Зарплата Ивана обновлена до 60 000")

    # 5. Удаляю Анну
    cursor.execute("DELETE FROM employees WHERE name = 'Анна'")
    conn.commit()
    print("Анна удалена из таблицы")

    # 3. Вывожу сотрудников с зарплатой > 50 000 (финальный результат)
    cursor.execute("SELECT name, position, salary FROM employees WHERE salary > 50000")
    high_paid = cursor.fetchall()
    print("Сотрудники с зарплатой больше 50 000:")
    for employee in high_paid:
        print(f"Имя: {employee[0]}, Должность: {employee[1]}, Зарплата: {employee[2]}")

    cursor.close()
    conn.close()
    print("Готово!")

except Exception as e:
    print(f"Ошибка: {e}")