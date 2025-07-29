"""""" # start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'openbabel_wheel.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-openbabel_wheel-3.1.1.22')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-openbabel_wheel-3.1.1.22')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

import sys
import warnings
import os
if os.name == 'nt':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.add_dll_directory(os.path.join(base_dir, "bin"))


from . import openbabel

__version__ = "3.1.0"

if "ON" == "ON":
    import os
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.environ["BABEL_LIBDIR"] = os.path.join(base_dir, "lib", "openbabel", __version__)
    os.environ["BABEL_DATADIR"] = os.path.join(base_dir, "share", "openbabel", __version__)

_thismodule = sys.modules[__name__]

class OBProxy(object):
    def __getattr__(self, name):
        if hasattr(_thismodule, name):
            return getattr(_thismodule, name)
        elif hasattr(openbabel, name):
            warnings.warn('"import openbabel" is deprecated, instead use "from openbabel import openbabel"')
            return getattr(openbabel, name)
        else:
            raise AttributeError

sys.modules[__name__] = OBProxy()
