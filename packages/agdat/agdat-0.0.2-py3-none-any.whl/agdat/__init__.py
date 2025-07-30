from copy import deepcopy as CopyObj

SEP = "\\"

def IsTypeOK(obj):
    if obj == None:
        return True
    if isinstance(obj, (int, float, str, bytes)):
        return True
    elif isinstance(obj, (list, tuple, set)):
        for i in obj:
            if not IsTypeOK(i):
                return False
        return True
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if not (IsTypeOK(k) and IsTypeOK(v)):
                return False
        return True
    else:
        return False

def IsNameOK(name):
    if not isinstance(name, str):
        return False
    else:
        return SEP not in name

def SplitBy(name: str, ind: int=1):
    if ind < 0:
        ind = len(name) - ind - 1
    pos = 0
    count = 0
    for i, t in enumerate(name):
        if t == SEP:
            count += 1
        if count == ind - 1:
            pos = i + 1
    return name[0: pos], name[pos+1:]

def SplitBy(name: str, ind: int=1):
    x = name.split(SEP)
    return SEP.join(x[0:ind]), SEP.join(x[ind:])

def Join(*names: str):
    return SEP.join(names).strip(SEP)

VALUE_TYPE_INVALID = TypeError("An Ag value should be None, int, str, bytes, float, or a list, tuple or set containing the types above, or a dict with these types as its keys and values.")
CONTAINS_INVALID = TypeError("An Ag containings for a AgDir should be a dict with valid names as keys and AgFile/AgDir as values.")
NAME_INVALID = TypeError("A valid Ag name should be a str without \"\\\"")
NAME_REPEATED = ValueError("The name already exists")

class AgObj:
    pass

class AgFile(AgObj):
    def __init__(self, value) -> None:
        self.SetValue(value)
    
    def SetValue(self, value):
        if IsTypeOK(value):
            self.value = CopyObj(value)
        else:
            raise VALUE_TYPE_INVALID
    
    def QueryValue(self):
        return CopyObj(self.value)
    
    def __repr__(self):
        return f"AgFile({repr(self.value)})"

class AgDir(AgObj):
    def __init__(self, contains: dict):
        self._SetContains(contains)
    
    def _SetContains(self, contains: dict):
        for k, v in contains.items():
            if (not IsNameOK(k)) or (not isinstance(v, AgObj)):
                raise CONTAINS_INVALID
        self.contains = CopyObj(contains)

    def Rename(self, old: str, new: str):
        if not IsNameOK(new):
            raise NAME_INVALID
        else:
            if old==new:
                return
            elif new in self.EnumAll(SplitBy(old, -1)[0]):
                raise NAME_REPEATED
            else:
                if SEP not in old:
                    val = self.contains[old]
                    del self.contains[old]
                    self.contains[new] = val
                else:
                    a, b = SplitBy(old)
                    self.contains[a].Rename(b, new)
    
    def SetValue(self, name: str, val):
        if SEP not in name:
            if name not in self.EnumAll():
                self.contains[name] = AgFile(val)
            else:
                self.contains[name].SetValue(val)
        else:
            a, b = SplitBy(name)
            self.contains[a].SetValue(b, val)
    
    def QueryValue(self, name: str):
        if SEP not in name:
            return self.contains[name].QueryValue()
        else:
            a, b = SplitBy(name)
            return self.contains[a].QueryValue(b)
    
    def _Enum(self, name: str="", typ: type=AgObj) -> list[str]:
        if name:
            if SEP in name:
                a, b = SplitBy(name)
            else:
                a, b = name, ""
            return self.contains[a]._Enum(b, typ)
        else:
            return [x for x in self.contains.keys() if isinstance(self.contains[x], typ)]
    
    def EnumAll(self, name: str="") -> list[str]:
        return self._Enum(name)
    
    def EnumDirs(self, name: str="") -> list[str]:
        return self._Enum(name, AgDir)
    
    def EnumFiles(self, name: str="") -> list[str]:
        return self._Enum(name, AgFile)
    
    def MkDir(self, name: str):
        if SEP in name:
            a, b = SplitBy(name)
            self.contains[a].MkDir(b)
        else:
            if IsNameOK(name):
                if name in self.EnumAll():
                    raise NAME_REPEATED
                else:
                    self.contains[name] = AgDir({})
            else:
                raise NAME_INVALID
    
    def MakeDirs(self, name: str):
        if SEP not in name:
            self.MkDir(name)
        else:
            a, b = SplitBy(name)
            if not self.IsDir(a):
                self.MkDir(a)
            self.contains[a].MakeDirs(b)
    
    def _Has(self, name: str, typ: type=AgObj) -> bool:
        if SEP in name:
            a, b = SplitBy(name)
            if a in self.EnumAll():
                if a in self.EnumFiles():
                    return False
                else:
                    return self.contains[a]._Has(b, typ)
            else:
                return False
        else:
            if name in self.EnumAll():
                return isinstance(self.contains[name], typ)
            else:
                return False

    def IsDir(self, name: str):
        return self._Has(name, AgDir)

    def IsFile(self, name: str):
        return self._Has(name, AgFile)
    
    def Exists(self, name: str):
        return self._Has(name)
    
    def Remove(self, name):
        if SEP in name:
            a, b = SplitBy(name)
            self.contains[a].Remove(b)
        else:
            del self.contains[name]
    
    def Attach(self, sth: AgObj, name: str):
        if not self.Exists(name):
            if SEP in name:
                a, b = SplitBy(name)
                self.contains[a].Attach(sth, b)
            else:
                if not IsNameOK(name):
                    raise NAME_INVALID
                else:
                    self.contains[name] = CopyObj(sth)
        else:
            raise NAME_REPEATED
    
    def GetSubDirCopy(self, name: str) -> "AgDir":
        if SEP in name:
            a, b = SplitBy(name)
            return self.contains[a].GetSubDirCopy(b)
        else:
            return CopyObj(self.contains[name])
    
    def TryQueryValue(self, name: str, default=None):
        try:
            return self.QueryValue(name)
        except:
            return default

    def __repr__(self):
        return f"AgDir({repr(self.contains)})"

def CreateAg():
    return AgDir({})

def LoadAgStr(msg: str) -> AgDir:
    from json import loads
    return eval(loads(msg))

def LoadAgFileName(filename: str|bytes):
    with open(filename, "r") as f:
        return LoadAgStr(f.read())

def LoadAgFileObj(fileobj):
    return LoadAgStr(fileobj.read())

def SaveAgStr(lib: AgDir):
    from json import dumps
    return dumps(repr(lib))

def SaveAgFileName(lib: AgDir, filename: str|bytes):
    with open(filename, "w") as f:
        f.write(SaveAgStr(lib))

def SaveAgFileObj(lib: AgDir, fileobj):
    fileobj.write(SaveAgStr(lib))

def READ_BYTES(fn: str):
    with open(fn, "rb") as f:
        return f.read()

def LoadPathAsAg(path: str, fileHandler=READ_BYTES):
    from os.path import isdir, isfile
    lib = CreateAg()
    allpaths = _Search(path)
    dirs = (x for x in allpaths if isdir(x))
    fils = (x for x in allpaths if isfile(x))
    for d in dirs:
        lib.MakeDirs(d)
    for f in fils:
        lib.SetValue(f, fileHandler(f))
    return lib

def _Search(path: str) -> list[str]:
    from os import listdir
    from os.path import isdir, join
    res = [path]
    for fn in listdir(path):
        subp = join(path, fn)
        if isdir(subp):
            res.extend(subp)
        else:
            res.append(subp)
    return res