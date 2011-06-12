
class Errors(dict):
    """
    A light wrapper for a dict, where keys are accessed as attributes.
    
    Used inside a model to store any errors (i.e. validation errors) so we 
    can do things like check for field errors in templates without 
    getting AttributeErrors.
    """
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            return None
