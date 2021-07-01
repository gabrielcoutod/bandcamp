from setuptools import setup

setup(name="bandcamp downloader",
      author="Gabriel Couto Domingues",
      license="MIT",
      install_requires=[
          "eyed3",
          "beautifulsoup4",
          "requests",
      ],
      zip_safe=False)
