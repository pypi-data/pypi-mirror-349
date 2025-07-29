# get the version
from importlib.metadata import version

__version__ = version('xcfr')
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

