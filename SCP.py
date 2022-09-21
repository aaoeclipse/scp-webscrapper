import pandas as pd

class SCP:
    def __init__(self, scp, item, object_class, containment_procedure, desc, rating, image=None):
        self.scp = scp
        self.item = item
        self.object_class = object_class
        self.containment_procedure = containment_procedure
        self.desc = desc
        self.rating = rating
        self.image = image
    
    def get_obj(self) -> dict:
        return pd.DataFrame({
            "SCP": [self.scp],
            "item": [self.item],
            "object_class" : [self.object_class],
            "containment_procedure" : [self.containment_procedure],
            "desc" : [self.desc],
            "rating": [self.rating],
            "image" : [self.image]
        })