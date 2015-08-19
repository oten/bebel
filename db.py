import os
import shutil
from subprocess import call, Popen, PIPE


class Table(object):
    def __init__(self, name, path='./'):
        if name == 'escher':
            raise Exception("'escher' is not a valid table name.")
        else:
            self._file_path = os.path.join(path, name + '.py')

            if not os.path.exists(self._file_path):
                shutil.copyfile('./escher.py', self._file_path)
                os.chmod(self._file_path, 0o777)
    
    def __getitem__(self, key):
        return self._read(key)

    def __setitem__(self, key, value):
        if hasattr(self, 'call_on_setitem'):
            self.call_on_setitem(self, key, value)
        self._write(key, value)

    def _read(self, key):
        if not isinstance(key, basestring):
            raise Exception("Key must be instance of 'basestring'.")

        pipe = Popen([self._file_path, key], stdout=PIPE, stderr=PIPE)
        value, err = pipe.communicate()
        if not err:
            return eval(value[:-1])

    def _write(self, key, value):
        if not isinstance(key, basestring):
            raise Exception("Key must be instance of 'basestring'.")

        value = repr(value)
        err = call([self._file_path, key, value])

    def keys(self):
        pipe = Popen([self._file_path], stdout=PIPE, stderr=PIPE)
        value, err = pipe.communicate()
        return value.split('\n')[:-1]

    def clear(self):
        err = call([self._file_path, '--clean'])

    def as_dict(self):
        return {k: self._read(k) for k in self.keys()}


class TransversalItem(object):
    def __init__(self, model, idx):
        for k, v in model.__class__.__dict__.items():
            if 'Table' in repr(v):  # Qualquer dia arrumo...
                self.__dict__.update({k: v[idx]})
        self.idx = idx
        self._model = model
    
    def __setattr__(self, attr, v):
        if hasattr(self, '_model'):
            self._model.__getattribute__(attr)[self.idx] = v
            self.__dict__.update({attr: v})
        else:
            super(TransversalItem, self).__setattr__(attr, v)
    
    def __repr__(self):
        return ', '.join(["%s -> %s" % (k, v) for k, v in \
                            self.__dict__.items() if k != '_model'])
            
        
class TransversalModel(object):
    def __getitem__(self, idx):
        return TransversalItem(self, idx)
    
    def add(self, idx, **kwarg):
        item = TransversalItem(self, idx)
        for k in kwarg:
            item.__setattr__(k, kwarg[k])


def Mirror(table):
    d = {}
    for k, v in table.as_dict().items():
        for i in v:
            d.get(i).add(k) if d.get(i) else d.update({i: set(k)}) 
    
    def fun(self, key, value):
        for k in d:
            d[k].discard(key)
        for i in value:
            d.get(i).add(key) if d.get(i) else d.update({i: set([key])})
    
    table.call_on_setitem = fun
    return d
    
