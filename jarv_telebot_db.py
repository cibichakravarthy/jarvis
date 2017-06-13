import sqlite3

class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text,cht int)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text,cht):
       stmt = "INSERT INTO items (description,cht) VALUES (?,{})".format(cht)
       args = (item_text,)
       self.conn.execute(stmt,args);
       self.conn.commit()

    def delete_item(self, item_text,cht):
       stmt = "DELETE FROM items WHERE description = (?) AND cht = {}".format(cht);
       args = (item_text, );        
       self.conn.execute(stmt, args)
       self.conn.commit()

    def get_items(self,cht):
        stmt = "SELECT description FROM items where cht={}".format(cht);
        return [x[0] for x in self.conn.execute(stmt)]
