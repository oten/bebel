import db

    
class Codes(db.TransversalModel):
    code = db.Table('code', path='./db')
    language = db.Table('language', path='./db')
    tags = db.Table('tags', path='./db')
    codes_of_tag = db.Mirror(tags)
    
    def __init__(self):
        if self.code.keys():
            self.next_idx = max(map(int, self.code.keys())) + 1
        else:
            self.next_idx = 0
    
    def add(self, **kwarg):
        super(Codes, self).add(str(self.next_idx), **kwarg)
        self.next_idx += 1
