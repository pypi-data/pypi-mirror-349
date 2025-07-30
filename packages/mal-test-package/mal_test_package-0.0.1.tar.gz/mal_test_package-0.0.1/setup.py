import sys
from distutils.core import setup

if not any(cmd in sys.argv for cmd in ["sdist", "egg_info"]):
    raise Exception(
        """
        Installation terminated!
        This is a package created to verify mal. package analysis.
        This is the package not intended to be installed and highlight problems in your setup.
        """
    )

setup()
