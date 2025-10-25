import psycopg2
from psycopg2.extras import DictCursor


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password="",
            port=5432,
            dbname="db_tg"
        )
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.create_table()

    def create_table(self):
        """Создание таблицы если её нет"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE,
            username VARCHAR(100),
            full_name VARCHAR(200),
            height INTEGER,
            weight DECIMAL(5,2),
            age INTEGER,
            gender VARCHAR(10),
            goal VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def add_user(self, telegram_id, username, full_name, height, weight, age, gender, goal):
        """Добавление или обновление пользователя"""
        sql = """
        INSERT INTO users (telegram_id, username, full_name, height, weight, age, gender, goal) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (telegram_id) 
        DO UPDATE SET 
            username = EXCLUDED.username,
            full_name = EXCLUDED.full_name,
            height = EXCLUDED.height,
            weight = EXCLUDED.weight,
            age = EXCLUDED.age,
            gender = EXCLUDED.gender,
            goal = EXCLUDED.goal
        """
        self.cursor.execute(sql, (telegram_id, username, full_name, height, weight, age, gender, goal))
        self.conn.commit()

    def get_user(self, telegram_id):
        """Получение пользователя по telegram_id"""
        sql = "SELECT * FROM users WHERE telegram_id = %s"
        self.cursor.execute(sql, (telegram_id,))
        return self.cursor.fetchone()

    def close(self):
        """Закрытие соединения"""
        self.cursor.close()
        self.conn.close()


# Глобальный экземпляр базы данных
db = Database()