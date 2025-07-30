"""
Package initialization and public API exports for netviz_tools.

This package includes three main classes: DataManager, NetworkManager, and TimeSeries.
- DataManager: Handles the loading and processing of network data.
- NetworkManager: Represents a network and provides methods for analysis and visualization.
- TimeSeries: Represents a time series of network data and provides methods for analysis and visualization.
"""

try:
    # Python 3.13+
    from importlib.metadata import version as _get_version
    __version__ = _get_version("netviz-tools")
except (ImportError, Exception):
    # Fall back to a default version if metadata is not available
    __version__ = "0.1.1"

__author__ = "Tyson Johnson"
__email__  = "tjohns94@gmu.edu"
__license__ = "MIT"

from .data_manager import DataManager
from .network_manager import TradeNetwork as NetworkManager
from .time_series import TradeSeries as TimeSeries
from .utils import save_json, CONTINENT_COLORS

__all__ = [
    "DataManager",
    "NetworkManager",
    "TimeSeries",
    "save_json",
    "CONTINENT_COLORS", 
]
