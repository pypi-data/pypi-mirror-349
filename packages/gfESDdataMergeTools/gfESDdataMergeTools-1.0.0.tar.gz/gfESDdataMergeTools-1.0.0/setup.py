from setuptools import setup, find_packages

setup(
    name="gfESDdataMergeTools",
    version="1.0.0",
    author="Yang Ting",
    author_email="ting009@e.ntu.edu.sg",
    description="GUI Tool for Merging ESD Test Data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=["gfESDdataMergeTools", "gfESDdataMergeTools.scr"],
    package_dir={
        "gfESDdataMergeTools": "gfESDdataMergeTools",
        "gfESDdataMergeTools.scr": "gfESDdataMergeTools/scr"
    },
    package_data={
        "gfESDdataMergeTools": [
            "app_logo/*.ico",
            "app_logo/*.png",
            "app_logo/*.jpg"
        ]
    },
    install_requires=[
        "PyQt5>=5.15.4",
        "openpyxl>=3.0.0",
        "xlrd>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "gf-esd-merge = gfESDdataMergeTools.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)