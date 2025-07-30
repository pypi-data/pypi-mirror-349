from .core import Pyvmote

__version__ = "1.0.0"

# Al importar pyvmote, devuelve una instancia automáticamente
_instance = Pyvmote()
import sys
sys.modules[__name__] = _instance