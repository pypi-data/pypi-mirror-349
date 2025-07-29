from setuptools import setup

setup(

    name = "zModule",
    version = "1.0.1",
    description = "Nothing at the moment.",
    author = "zisia13",
    github = "zisia13",
    author_email = "nothing@nothing.com",
    packages = ["zModules", 
                "zModules.zBanner",
                "zModules.zOs",
                "zModules.zCryptography"
               ],
    install_requires = [],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)