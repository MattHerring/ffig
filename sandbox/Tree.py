from ctypes import *
c_object_p = POINTER(c_void_p)

class Tree:

  @property
  def right(self):
    ptr = conf.lib.Tree_right(self);
    if bool(ptr):
      return Tree(p=ptr)
    return None

  @property
  def left(self):
    ptr = conf.lib.Tree_left(self);
    if bool(ptr):
      return Tree(p=ptr)
    return None

  @property
  def data(self):
    return conf.lib.Tree_data(self);

  def from_param(self):
    return self.ptr

  def __del__(self):
    conf.lib.Tree_dispose(self)

  def __init__(self,n=0,p=None):
    if p:
      self.ptr = p
    else:
      self.ptr = conf.lib.Tree_create(n)

  @staticmethod
  def count():
      return conf.lib.Tree_count()

methodList = [

  ("Tree_dispose",
  [Tree],
  None),

  ("Tree_create",
  [c_int],
  c_object_p),

  ("Tree_right",
  [Tree],
  c_object_p),

  ("Tree_left",
  [Tree],
  c_object_p),

  ("Tree_data",
  [Tree],
  c_int),

  ("Tree_count",
  [],
  c_int)
]

# library loading and method registrations
# based on clang python bindings approach

def register_method(lib, item):
  func = getattr(lib, item[0])

  if len(item) >= 2:
    func.argtypes = item[1]

  if len(item) >= 3:
    func.restype = item[2]


class CachedProperty(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        value = self.wrapped(instance)
        setattr(instance, self.wrapped.__name__, value)

        return value

class Config:
    library_path = None
    loaded = False

    @staticmethod
    def set_library_path(path):
        if Config.loaded:
            raise Exception("library path is already set.")
        Config.library_path = path

    @CachedProperty
    def lib(self):
        lib = self._get_library()
        map(lambda x:register_method(lib,x), methodList)
        Config.loaded = True
        return lib

    def _get_filename(self):
        import platform
        name = platform.system()

        if name == 'Darwin':
            file = 'libTree_c.dylib'
        elif name == 'Windows':
            file = 'Tree_c.dll'
        else:
            file = 'libTree_c.so'

        if Config.library_path:
            file = Config.library_path + '/' + file

        return file

    def _get_library(self):
        try:
            library = cdll.LoadLibrary(self._get_filename())
        except OSError as e:
            msg = str(e) + ". To provide a path to Tree dylib use Config.set_library_path()"
            raise Exception(msg)

        return library

conf = Config()


