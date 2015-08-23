#coding: utf-8
import db

    
class Codes(db.TransversalModel):
    code = db.Table('codes_code', path='./db')
    language = db.Table('codes_language', path='./db')
    tags = db.Table('codes_tags', path='./db')
    codes_of_tag = db.Mirror(tags)
    codes_of_language = db.Mirror(language)
    
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
        yield idx
        if lst:
            for k in self[idx]:
                for j in self.search(k): # yield from self.search(k)
                    yield j

    def pretty_print(self, idx, offset='', last=True):
        lst = self[idx]
        print offset,
        if last:
            print " └─",
            level = offset + "   "
        else:
            print " ├─",
            level = offset + "  │"
        print idx
        if lst:
            for k in lst:
                self.pretty_print(k, level, last=(k == lst[-1]))
