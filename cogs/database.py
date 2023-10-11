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
    
    def query(self, query, data:tuple=None):
        try:
            self.cursor.execute(query, data)
        except mysql.connector.Error as err:
            return err
        finally:
            self.cursor.commit()
    
    def fetch(self, query, data:tuple=None, fetchmany=None, fetchone:bool=True, fetchall:bool=False):
        if fetchall is not False or fetchmany is not None:
            if isinstance(fetchmany, int):
                try:
                    self.cursor.execute(query, data)
                    return self.cursor.fetchmany(fetchmany)
                except mysql.connector.Error as err:
                    return err
                finally:
                    self.cursor.commit()
            elif fetchall is True:
                try:
                    self.cursor.execute(query, data)
                    return self.cursor.fetchall()
                except mysql.connector.Error as err:
                    return err
                finally:
                    self.cursor.commit()
        else:
            try:
                self.cursor.execute(query, data)
                return self.cursor.fetchone()
            except mysql.connector.Error as err:
                return err
            finally:
                self.cursor.commit()
    
    def insert(self, query, data: tuple):
        try:
            self.cursor.execute(query, data)
        except mysql.connector.Error as err:
            return err
        finally:
            self.cursor.commit()
            
            # Going to cut time in half when doing DB transactions using these functions
            # ALSO is alot safer - might integrate an argument check function to make sure that the query is valid compared to the function they called making the code a lot
            # more safe. CBA for the DB to be corrupted or keep messing up.
