from database import create_connection
import mysql.connector

class User:
    @staticmethod
    def get_by_email(email):
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(name, email, hashed_password, role, horizon):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user (name, email, password, role, horizon) VALUES (%s, %s, %s, %s, %s)",
                (name, email, hashed_password, role, horizon)
            )
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all():
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM user")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(user_id, name, email, role, horizon, hashed_password=None):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            if hashed_password:
                cursor.execute(
                    "UPDATE user SET name=%s, email=%s, password=%s, role=%s, horizon=%s WHERE id=%s",
                    (name, email, hashed_password, role, horizon, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE user SET name=%s, email=%s, role=%s, horizon=%s WHERE id=%s",
                    (name, email, role, horizon, user_id)
                )
            conn.commit()
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(user_id):
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
            conn.commit()
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()