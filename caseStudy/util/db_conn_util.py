import mysql.connector
from util.db_property_util import DBPropertyUtil
from exception.database_connection_exception import DatabaseConnectionException

class DBConnUtil:
    @staticmethod
    def get_connection():
        connection_string = DBPropertyUtil.get_connection_string("db.properties")
        try:
            conn = mysql.connector.connect(**connection_string)
            return conn
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            raise DatabaseConnectionException("Failed to establish database connection.")