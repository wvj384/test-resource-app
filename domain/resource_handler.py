class ResourceHandler:
    
    def get_type(self, params):
        return {"name":"type1", "max_speed":100}

    def create_type(self, object):
        return True

    def update_type(self, params, object):
        return True
    
    def delete_type(self, params):
        return True

    def get_resource(self, params):
        return {"name":"resource1", "type":"type1", "speed":90}
    
    def create_resource(self, object):
        return True

    def update_resource(self, params, object):
        return True
    
    def delete_resource(self, params):
        return True
    
    