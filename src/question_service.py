import os
import mysql.connector


# Singleton connection instance
_db_connection_instance = None


class _DatabaseConnection:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Successfully connected to the database")

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            self.connection = None
            print("MySQL connection is closed")

    def fetch_questions(self, question_id=None):
        self.connect()
        if question_id is None:
            query = "SELECT id, question_text FROM question"
            self.cursor.execute(query)
        else:
            query = "SELECT id, question_text FROM question WHERE id = %s"
            self.cursor.execute(query, (question_id,))

        questions = self.cursor.fetchall()
        for question in questions:
            print(f"ID: {question[0]}, Question: {question[1]}")
        return questions

    def insert_question(self, question_id, question_text):
        self.connect()

        query = "INSERT INTO question (id, question_text) VALUES (%s, %s)"
        self.cursor.execute(query, (question_id, question_text))
        self.connection.commit()

        inserted_successfully = True
        print(f"Question inserted with ID: {question_id}")


def get_db_connection_instance():
    global _db_connection_instance
    if _db_connection_instance is None:
        _db_connection_instance = _DatabaseConnection(host=os.getenv('API_DB_HOST'),
                                                      port=os.getenv('API_DB_PORT'),
                                                      user='root',
                                                      password=os.getenv('MYSQL_ROOT_PASSWORD'),
                                                      database=os.getenv('MYSQL_DATABASE'))
    return _db_connection_instance


# Usage
if __name__ == "__main__":
    db = get_db_connection_instance()
    try:
        db.fetch_questions()  # Fetch all questions
        db.fetch_questions("q10")  # Fetch a specific question by ID
    finally:
        db.disconnect()
