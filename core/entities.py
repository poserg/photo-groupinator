class Image(object):
    
    def __init__(self, name, path):
        self.name = name
        self.path = path
        
    def __repr__(self):
        return "<Image('%s', '%s')>" % (self.name, self.path)
        
class Group(Image):
    
    def __repr__(self):
        return "<Group('%s')>" % (self.name)

class ImageGroup(object):

    def __init__(self, image_id, group_id):
        self.image_id = image_id
        self.group_id = group_id

class OperationType(object):

    def __init__(self, name):
        self.name = name

class Operation(object):

    def __init__(self, name, operation_type_id):
        pass

class OperationGroup(object):

    def __init__(self, operation_id, group_id):
        self.operation_id = operation_id
        self.group_id = group_id
