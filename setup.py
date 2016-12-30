from setuptools import setup, find_packages
from ztool.main import __name__,__author__,__email__,__version__,__url__

setup(
      name=__name__,
      version=__version__,
      description="ztool",
      author=__author__,
      author_email=__email__,
      url=__url__,
      license="LGPL",
      packages= find_packages(),
      )
