import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Customer(threading.Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        print(f"Посетитель номер {self.number} прибыл")
        table = self.cafe.serve_customer(self)
        time.sleep(5)  # время на еду
        print(f"Посетитель номер {self.number} покушал и ушёл.")
        table.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.queue = queue.Queue()
        self.tables = tables

    def customer_arrival(self):
        customer_number = 1
        while customer_number < 21:  # ограничение на 20 посетителей
            time.sleep(1)  # интервал прибытия посетителей
            customer = Customer(customer_number, self)
            if any(not table.is_busy for table in self.tables):
                customer.start()
                customer_number += 1
            else:
                self.queue.put(customer_number)
                print(f"Посетитель номер {customer_number} ожидает свободный стол.")
                customer_number += 1

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.number} сел за стол {table.number}.")
                return table
        print(f"Посетитель номер {customer.number} сел за стол N.")

# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
