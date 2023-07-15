import os
import json
import mysql.connector


connection = None
cursor = None


def initialize():
    connect()
    create_photo_table()


def connect():
    global connection
    global cursor
    connection = mysql.connector.connect(
        host=os.environ["HOST"],
        database=os.environ["DATABASE"],
        user=os.environ["USER"],
        password=os.environ["PASSWORD"],
    )
    cursor = connection.cursor()


def close():
    cursor.close()
    connection.close()


def create_photo_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            id INT NOT NULL AUTO_INCREMENT,
            uid VARCHAR(500) NOT NULL,
            name VARCHAR(500) NOT NULL,
            content_type VARCHAR(100) NOT NULL,
            src TEXT NOT NULL,
            labels TEXT NOT NULL,
            word2vec TEXT NOT NULL,
            PRIMARY KEY (id)
        );
        """
    )
    connection.commit()


def delete_photos():
    cursor.execute("DELETE FROM photos;")
    connection.commit()


def add_photo(uid, name, content_type, src, labels, word2vec):
    cursor.execute(
        f"""
        INSERT INTO photos (uid, name, content_type, src, labels, word2vec) 
        VALUES (
            '{uid}', 
            '{name}', 
            '{content_type}', 
            '{src}', 
            '{json.dumps(labels)}', 
            '{json.dumps(word2vec)}');
        """
    )
    connection.commit()


def select_photos(uid):
    cursor.execute(f"SELECT * FROM photos WHERE uid = '{uid}';")
    return [
        {
            "id": row[0],
            "uid": row[1],
            "name": row[2],
            "content_type": row[3],
            "src": row[4],
            "labels": row[5],
            "word2vec": row[6],
        }
        for row in cursor
    ]
