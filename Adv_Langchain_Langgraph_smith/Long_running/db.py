import sqlite3

DB="workflow.db"

def conn():
    return sqlite3.connect(DB)

def init():
    c=conn()
    c.execute("""CREATE TABLE IF NOT EXISTS workflow(
        key TEXT PRIMARY KEY,
        value TEXT
    )""")
    c.commit()
    c.close()

def set_value(key,value):
    c=conn()
    c.execute("INSERT OR REPLACE INTO workflow VALUES(?,?)",(key,value))
    c.commit()
    c.close()

def get_value(key):
    c=conn()
    r=c.execute("SELECT value FROM workflow WHERE key=?",(key,)).fetchone()
    c.close()
    return r[0] if r else None
