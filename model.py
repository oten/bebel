#coding: utf-8
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
        self.parent = db.Mirror(self)
    
    def search(self, idx):
        lst = self[idx]
        if lst:
            for k in lst:
                for j in self.search(k): # yield from self.search(k)
                    yield j
        else:
            yield idx

    def pretty_print(self, idx, hide=set(), offset='', last=True):
        lst = self[idx]
        s = u''
        s += offset
        if last:
            s += u" └─"
            level = offset + u"   "
        else:
            s += u" ├─"
            level = offset + u" │ "
        s += idx + u"\n"
        if lst:
            if idx in hide:
                s += level + u"└─+\n"
                return s
            for k in lst:
                s += self.pretty_print(k, hide=hide, offset=level, last=(k == lst[-1]))
        return s
