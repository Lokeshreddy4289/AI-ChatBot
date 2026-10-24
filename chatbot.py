
import re

from database import get_connection
from ai_service import generate_sql


def ask_database(question):
    sql = generate_sql(question).strip()

    # Remove one optional trailing semicolon.
    sql = sql.rstrip(";").strip()

    # Allow only SELECT statements.
    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        return "Only SELECT queries are allowed."

    # Reject multiple statements.
    if ";" in sql:
        return "Multiple SQL statements are not allowed."

    # Block common modification and file-operation keywords.
    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|"
        r"REPLACE|GRANT|REVOKE|CALL|OUTFILE|DUMPFILE)\b",
        re.IGNORECASE
    )

    if forbidden.search(sql):
        return "The generated query contains a prohibited operation."

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    question = input("Ask your database: ")

    try:
        print(ask_database(question))
    except Exception as error:
        print("Error:", error)
