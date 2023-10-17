import psycopg2
from domain.errors import ResourceHandlerError
from ports.storage import Storage
from domain.model import ResourceType, Resource


class PostgresStorage(Storage):
    
    conn = None

    def __init__(self, host, port, dbname, user, password):
        self.conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)

    # Types

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
        
    def update_type(self, item):
        try:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE types SET name=%s, max_speed=%s WHERE id=%s',
                (item.name, item.max_speed, item.id)
            )
            self.conn.commit()
            return True, item
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None

    def get_types(self, ids):
        result = []
        query = "SELECT id, name, max_speed FROM types"
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

    def delete_types(self, ids):
        result = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM types WHERE id IN ({','.join(map(str, ids))}) RETURNING id, name, max_speed")
            data = cursor.fetchall()
            self.conn.commit()
            for (id, name, max_speed) in data:
                result.append(ResourceType(name, max_speed, id))
            return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None

    # Resources

    def create_resource(self, item):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO resources (name, type_id, speed) VALUES (%s, %s, %s) RETURNING id',
                (item.name, item.type.id, item.speed)
            )
            [id] = cursor.fetchone()
            self.conn.commit()
            result = Resource(item.name, item.type, item.speed, id)
            print(result.output)
            return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None
        
    def update_resource(self, item):
        try:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE resources SET name=%s, type_id=%s, speed=%s WHERE id=%s',
                (item.name, item.type.id, item.speed, item.id)
            )
            self.conn.commit()
            return True, item
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None
        
    def get_resources(self, ids):
        result = []
        query = """
            SELECT r.id, r.name, r.speed, t.id AS type_id, t.name AS type_name, t.max_speed 
            FROM resources r INNER JOIN types t ON t.id = r.type_id
        """
        if len(ids) > 0:
            query += f" WHERE r.id IN ({','.join(map(str, ids))})"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            for (id, name, speed, type_id, type_name, type_max_speed) in data:
                type = ResourceType(type_name, type_max_speed, type_id)
                result.append(Resource(name, type, speed, id))
            return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None
        
    def delete_resources(self, ids):
        result = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"""
                           DELETE FROM resources r USING types t WHERE t.id = r.type_id AND r.id IN ({','.join(map(str, ids))}) 
                           RETURNING r.id, r.name, r.speed, t.id, t.name, t.max_speed"""
                           )
            data = cursor.fetchall()
            print(data)
            self.conn.commit()
            for (id, name, speed, type_id, type_name, type_max_speed) in data:
                type = ResourceType(type_name, type_max_speed, type_id)
                result.append(Resource(name, type, speed, id))
            return True, result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False, None