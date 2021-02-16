from os import name
import sqlite3


class Database:
    def __init__(self, path_to_db='data/bot_users.db'):
        self.path_to_db = path_to_db
    
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute (
        self, 
        sql: str, 
        parameters: tuple = None, 
        fetchone = False,
        fetchall = False,
        commit = False 
        ):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data
    
    def create_table_users(self):
        sql = '''
            CREATE TABLE users (
                id int NOT NULL,
                name varchar(255) NOT NULL,
                status varchar(255),
                PRIMARY KEY (id)
            );
        '''
        self.execute(sql, commit=True)

    def add_user(self, id:int, name:str, status:str='request'):
        sql = '''
            INSERT INTO users (id, name, status) 
            VALUES (?, ?, ?)
        '''
        parameters = (id, name, status)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = '''SELECT * FROM users'''
        
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters:dict):
        sql += ' AND '.join([
            f'{item} = ?' for item in parameters
        ])

        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        sql = 'SELECT * FROM users WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters, fetchone=True)

    def update_status(self, status, id):
        sql = 'UPDATE users SET status = ? WHERE id = ?'

        return self.execute(sql, parameters=(status, id), commit=True)

    def delete_user(self, id):
        sql = 'DELETE FROM users WHERE id = ?'

        self.execute(sql, parameters=(id, ), commit=True)

    def delete_all_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    # def check_user(self, id):
    #     sql = 'SELECT * FROM user WHERE id = ?'

    #     return



def logger(statement):
    print (
        f'''
        ======================================
        Executing:
        {statement}
        ______________________________________
        '''
    )




def test():
    
    db = Database()
#     db.delete_user(154253)
    db.delete_all_users()
    
#     #db.create_table_users()
#     #db.add_user(452145, "Konstantine", "andmin")
#     #db.add_user(154253, "Vasily", "permit")
#     db.update_status('admin', 154253)
    

    # users = db.select_all_users()
    # print(f"Получил всех пользователей: {users}")

    

    users = db.select_all_users()
    print(f"Получил всех пользователей: {users}")

    # user = db.select_user(name="John", id=5)
    # print(f"Получил пользователя: {user}")


test()