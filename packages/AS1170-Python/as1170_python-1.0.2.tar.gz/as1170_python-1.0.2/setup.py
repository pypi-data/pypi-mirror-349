from setuptools import setup, find_packages

setup(
    name="as1170",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["smbus2", "RPi.GPIO"],
    author="Alessandro Cursoli",
    author_email="alessandro.cursoli@supernovaindustries.it",
    description="Library to control AS1170 LED driver via I2C on Raspberry Pi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SupernovaIndustries/AS1170-Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
