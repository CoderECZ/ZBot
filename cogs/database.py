import mysql.connector as mysql
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    db_config = {
        'host': config['database']['host'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'database': config['database']['database'],
    }

class Database:
    def __init__(self):
        self.database = db_config
        self.connection = mysql.connector.connect(**self.database)
        self.cursor = self.connection.cursor()
    
    def query(self, query):
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            return err
        finally:
            self.cursor.commit()
            self.cursor.close()
    
    def fetch(self, query, fetchmany=None, fetchone:bool=True, fetchall:bool=False):
        if fetchall is not False or fetchmany is not None:
            if isinstance(fetchmany, int):
                try:
                    self.cursor.execute(query)
                    return self.cursor.fetchmany(fetchmany)
                except mysql.connector.Error as err:
                    return err
                finally:
                    self.cursor.commit()
            elif fetchall is True:
                try:
                    self.cursor.execute(query)
                    return self.cursor.fetchall()
                except mysql.connector.Error as err:
                    return err
                finally:
                    self.cursor.commit()
        else:
            try:
                self.cursor.execute(query)
                return self.cursor.fetchone()
            except mysql.connector.Error as err:
                return err
            finally:
                self.cursor.commit()
    
    def insert(self, query, data):
        try:
            self.cursor.execute(query, data)
        except mysql.connector.Error as err:
            return err
        finally:
            self.cursor.commit()
