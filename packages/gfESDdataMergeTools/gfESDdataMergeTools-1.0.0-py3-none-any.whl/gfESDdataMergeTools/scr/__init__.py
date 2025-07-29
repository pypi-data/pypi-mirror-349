"""
- mainwindow: This file define the main GUI.
- tlpdatamerge: This file define the TLP merge data.
- hbmdatamerge: This file define the HBM merge data.
"""

# Version information
__version__ = "1.0.0"

# Show all the classes
__all__ = [
    "MainWindow",
    "TLPDataMerge",
    "HBMDataMerge"
]

# Init all classes
try:
    # main window
    from .mainwindow import MainWindow
    
    # merge data
    from .tlpdatamerge import TLPDataMerge
    from .hbmdatamerge import HBMDataMerge

except ImportError as e:
    print(f"Error of import class: {str(e)}")
    raise

# Init source package
def _scr_package_init():
    """Pre-init"""
    import sys, os

    # Add source file to the system path
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    if pkg_dir not in sys.path:
        sys.path.insert(0, pkg_dir)

    try:
        import numpy
    except ImportError as e:
        print(f"Missing necessary dependencies: {str(e)}")
        raise

# Execute initialization
#_scr_package_init()

