import sqlite3,json
class SharedMemory:
    def __init__(self):
        self.conn=sqlite3.connect("shared_memory.db",check_same_thread=False)
        self.conn.execute('CREATE TABLE IF NOT EXISTS memory(session_id TEXT,key TEXT,value TEXT,PRIMARY KEY(session_id,key))')
        self.conn.commit()
    def write(self,s,k,v):
        self.conn.execute("INSERT OR REPLACE INTO memory VALUES(?,?,?)",(s,k,json.dumps(v)));self.conn.commit()
    def read(self,s,k):
        r=self.conn.execute("SELECT value FROM memory WHERE session_id=? AND key=?",(s,k)).fetchone()
        return json.loads(r[0]) if r else None
