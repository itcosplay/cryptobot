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

        return self.execute(sql, parameters, fetchall=True)

    def get_user_name(self, id):
        user = self.select_user(id=id)

        return user[0][1]

    def get_group_users(self):
        pass

    def select_id_users(self, **kwargs):
        sql = 'SELECT id FROM users WHERE '
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters, fetchall=True)

    def select_all_statuses(self):
        '''
        returns list of tuples with statuses
        [(status_1,), (status_2), ...]
        '''
        sql = 'SELECT DISTINCT status FROM users'

        return self.execute(sql, fetchall=True)

    def get_all_statuses(self):
        '''
        returns list of statuses
        ['status_1', 'status_2', ...]
        '''
        statuses = self.select_all_statuses()
        statuses = [item for t in statuses for item in t]
        
        return statuses

    def select_status_user(self, **kwargs):
        sql = 'SELECT status FROM users WHERE '
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

    


def logger(statement):
    print (
        f'''
        ======================================
        Executing:
        {statement}
        ______________________________________
        '''
    )




# def test():
    
    # db = Database()
    # db.delete_user(439453169)
    # db.delete_all_users()
    
    # db.create_table_users()
    # db.add_user(1637852195, "myTestUser", "admin")
    # db.add_user(111111, "Inna", "admin")
    # db.update_status('admin', 1637852195)
    # print(db.select_status_user(id=1637852195)[0])
    
    # print(db.get_user_name(1637852195))

    # превращаем список кортежей в список элементов
    # users - some [(tuple),...()()()]
    # user = [item for t in users for item in t][2]

    # print(user)
    # print(db.select_user(status='admin'))

    # users = db.select_all_users()
    # print(f"Получил всех пользователей: {users}")

    # bloked_users = db.select_id_users(status='block')
    # print(f"Получил пользователя: {bloked_users}")

    # db.delete_user(id=59677456)
    # users = db.select_all_users()
    # print(f"Получил всех пользователей: {users}")

    # print(db.get_all_statuses())



# test()