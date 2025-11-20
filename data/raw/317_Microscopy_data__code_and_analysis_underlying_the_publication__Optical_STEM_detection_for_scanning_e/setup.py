from setuptools import setup

DISTNAME = "Single beam OSTEM Demo"
DESCRIPTION = "Demonstration repository for single beam optical scanning electron microscopy (OSTEM)"
MAINTAINER = "Arent Kievits"
MAINTAINER_EMAIL = "a.j.kievits@tudelft.nl"
LICENSE = "LICENSE"
URL = "https://github.com/arentkievits/ostem"
VERSION = "0.1.dev"
PACKAGES = [
"code",
]
INSTALL_REQUIRES = [
    "jupyterlab",
    "ipython",
    "scipy",
    "scikit-image",
    "beautifulsoup4",
    "altair",
    "numpy",
    "tifffile",
    "seaborn",
    "tqdm",
    "lxml",
    "ipywidgets",
    "ipympl",
]

if __name__ == '__main__':

    setup(
        name=DISTNAME,
        version=VERSION,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        packages=PACKAGES,
        include_package_data=False,
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=open("README.md").read(),
        install_requires=INSTALL_REQUIRES,
    )
