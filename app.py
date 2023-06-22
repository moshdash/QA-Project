import mysql.connector


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pa$$w0rd",
            auth_plugin="mysql_native_password",
            database="test_scores"
        )
        self.cursor = self.conn.cursor()

        # Create the database if it doesn't exist
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS test_scores")
        self.conn.database = "test_scores"

        # Create the table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                subject VARCHAR(255),
                score INT,
                percentage FLOAT
            )
        """)

    def insert_score(self, name, subject, score):
        percentage = (score / 100) * 100

        insert_query = """
            INSERT INTO scores (name, subject, score, percentage)
            VALUES (%s, %s, %s, %s)
        """
        values = (name, subject, score, percentage)

        self.cursor.execute(insert_query, values)
        self.conn.commit()

    def get_score_by_name(self, name):
        select_query = """
            SELECT subject, score, percentage
            FROM scores
            WHERE name = %s
        """
        value = (name,)

        self.cursor.execute(select_query, value)
        result = self.cursor.fetchall()

        if result:
            print(f"Test scores for {name}:")
            for row in result:
                subject, score, percentage = row
                print(
                    f"Subject: {subject}, Score: {score}/100, Percentage: {percentage}%")
        else:
            print(f"No test scores found for {name}.")

    def __del__(self):
        self.cursor.close()
        self.conn.close()


def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def main():
    db = Database()

    name = input("Enter your name: ")

    subjects = ["ICT", "MATHS", "CHEMISTRY"]
    for subject in subjects:
        score = get_int_input(
            f"Enter your {subject} test score (out of 100): ")
        db.insert_score(name, subject, score)

    option = input("Do you want to view your test scores? (Y/N): ")
    if option.upper() == "Y":
        db.get_score_by_name(name)


if __name__ == "__main__":
    main()
