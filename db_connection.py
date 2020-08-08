from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import pymysql
import os

def load_db():
    load_dotenv()
    encs_user = os.getenv("ENCS_USR")
    encs_password = os.getenv("ENCS_PWD")
    db_user = os.getenv("DB_USR")
    db_password = os.getenv("DB_PWD")

    db_host = 'oxc353.encs.concordia.ca'
    with SSHTunnelForwarder(
        ('login.encs.concordia.ca', 22),
        ssh_username=encs_user,
        ssh_password=encs_password,
        remote_bind_address=(db_host, 3306)
    ) as tunnel:
        port = tunnel.local_bind_port
        db_connection = pymysql.connect(
            host='localhost', port=port, db='oxc353_1', user=db_user,
            password=db_password, charset='utf8mb4')
        cursor = db_connection.cursor()
        cursor.execute("USE oxc353_1")
        cursor.execute("SELECT * FROM MP_User")
        for table in cursor:
            print(table)


def search_postings(title, category):
    if title is None:
        title = ""
    if category is None:
        category = ""
    data = []
    load_dotenv()
    encs_user = os.getenv("ENCS_USR")
    encs_password = os.getenv("ENCS_PWD")
    db_user = os.getenv("DB_USR")
    db_password = os.getenv("DB_PWD")

    db_host = 'oxc353.encs.concordia.ca'
    with SSHTunnelForwarder(
        ('login.encs.concordia.ca', 22),
        ssh_username=encs_user,
        ssh_password=encs_password,
        remote_bind_address=(db_host, 3306)
    ) as tunnel:
        port = tunnel.local_bind_port
        db_connection = pymysql.connect(
            host='localhost', port=port, db='oxc353_1', user=db_user,
            password=db_password, charset='utf8mb4')
        cursor = db_connection.cursor()
        cursor.execute("USE oxc353_1")
        query = "SELECT * FROM MP_Job_posting " \
                "WHERE job_title LIKE '% " + title + "%' " \
                "AND description LIKE '%" + title + "%' " \
                "AND category LIKE '%" + category+"%';"
        cursor.execute(query)
        for table in cursor:
            data.append(table)
            # print(table)
        db_connection.close()
        return data
