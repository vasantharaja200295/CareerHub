import configparser

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        connection_string = {
            "host": config.get("database", "host"),
            "user": config.get("database", "user"),
            "password": config.get("database", "password"),
            "database": config.get("database", "database")
        }
        return connection_string