import db

    
class Codes(db.TransversalModel):
    code = db.Table('codes_code', path='./db')
    language = db.Table('codes_language', path='./db')
    tags = db.Table('codes_tags', path='./db')
    codes_of_tag = db.Mirror(tags)
    
    def __init__(self):
        if self.code.keys():
            self.next_idx = max(map(int, self.code.keys())) + 1
        else:
            self.next_idx = 0
    
    def add(self, **kwarg):
        super(Codes, self).add(str(self.next_idx), **kwarg)
        self.next_idx += 1


class Tags(db.Table):
    def __init__(self):
        super(Tags, self).__init__('tags', path='./db')

    def search(self, idx):
        lst = self[idx]
        if not lst:
            return idx
        else:
            tmp = list()
            for k in lst:
                v = self.search(k)
                if type(v) == list:
                    for i in v:
                        tmp.append(i)
                else:
                    tmp.append(v)
            return tmp
            
