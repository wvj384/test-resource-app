class ResourceHandlerError(Exception):
    type = 'unknown'
    def __init__(self, type, *args):
        super().__init__(args)
        self.type = type

    def __str__(self):
        return f'{self.type}'
    
UNKNOWN_DB_ERROR = 'unknown db error'
BAD_ITEM_ERROR = 'bad item error'
INVALID_TYPE_ERROR = 'invalid type_id error'
INVALID_ID_ERROR = 'invalid id error'