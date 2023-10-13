class ResourceHandler:
    
    def get_type(self, id):
        return {"name":"type1", "max_speed":100}
    
    def update_type(self, id, object):
        return True
    
    def delete_type(id):
        return True

    def get_resource(self, id):
        return {"name":"resource1", "type":"type1", "speed":90}

    def update_resource(self, id, object):
        return True
    
    def delete_resource(id):
        return True
    
    