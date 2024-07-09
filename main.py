import psycopg2

db_params = {
    'database': 'jamoliddin',
    'user': 'postgres',
    'password': '0707',
    'host': 'localhost',
    'port': 5433
}


class Database:
    def __init__(self, params):
        self.params = params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.params)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()


class Book:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS kitoblar
        (
            id             SERIAL PRIMARY KEY,
            nomi           VARCHAR(100) NOT NULL,
            muallifi       VARCHAR(100) NOT NULL,
            sana           INTEGER
        )
        """
        self.cursor.execute(query)

    def insert_book(self, nomi, muallifi, sana):
        query = "INSERT INTO kitoblar (nomi, muallifi, sana) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (nomi, muallifi, sana))

    def get_books(self):
        query = "SELECT * FROM kitoblar"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_book(self, kitob_id, nomi=None, muallifi=None, sana=None):
        updates = []
        query_params = []

        if nomi:
            updates.append("nomi = %s")
            query_params.append(nomi)
        if muallifi:
            updates.append("muallifi = %s")
            query_params.append(muallifi)
        if sana:
            updates.append("sana = %s")
            query_params.append(sana)

        query_params.append(kitob_id)
        query = f"UPDATE kitoblar SET {', '.join(updates)} WHERE id = %s"
        self.cursor.execute(query, tuple(query_params))

    def delete_book(self, kitob_id):
        query = "DELETE FROM kitoblar WHERE id = %s"
        self.cursor.execute(query, (kitob_id,))


with Database(db_params) as cursor:
    book = Book(cursor)

    book.create_table()

    book.insert_book("Python dasturlash tilida o'rganish", "Jamoliddin Shodmonov", 2024)

    books = book.get_books()
    print("Barcha kitoblar:")
    for b in books:
        print(b)

    book.update_book(1, nomi=input("Yangilangan nom: "))

    book.delete_book(1)
