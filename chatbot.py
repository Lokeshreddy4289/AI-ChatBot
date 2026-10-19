import re
from database import get_connection
from ai_service import generate_sql

def ask_database(question):
    sql = generate_sql(question)

    # Allow SELECT queries only
    if not re.match(r"^\s*SELECT\b", sql, re.IGNORECASE):
        return "Only SELECT queries are allowed."

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    finally:
        if cursor:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    question = input("Ask your database: ")
    try:
        print(ask_database(question))
    except Exception as error:
        print("Error:", error)