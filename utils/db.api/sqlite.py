import sqlite3


class Database:
    def __init__(self, path_to_db='bot_users.db'):
        self.path_to_db = path_to_db
    
    @property
    def connection(self):
        return sqlite3.connect(self, path_to_db)

    def execute (
        self, 
        sql: str, 
        parameters: tuple = None, 
        fetchone = False,
        fetchall = False,
        commit = False 
        ):
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

    def select_user(self, **kwargs):
        sql = '''
            SELECT * FROM users WHERE

        '''



def logger(statement):
    print (
        f'''
        ======================================
        Executing:
        {statement}
        ______________________________________
        '''
    )