import psycopg2
from ports.storage import Storage
from domain.model import ResourceType


class PostgresStorage(Storage):
    
    conn = None

    def __init__(self, host, port, dbname, user, password):
        self.conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)

    def get_types(self, ids):
        result = []
        query = "SELECT * FROM types"
        if len(ids) > 0:
            query += f" WHERE id IN ({','.join(map(str, ids))})"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            for (id, name, max_speed) in data:
                result.append(ResourceType(name, max_speed, id))
            return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None

    def create_type(self, item):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO types (name, max_speed) VALUES (%s, %s) RETURNING id',
                (item.name, item.max_speed)
            )
            [id] = cursor.fetchone()
            self.conn.commit()
            result = ResourceType(item.name, item.max_speed, id)
            return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None
