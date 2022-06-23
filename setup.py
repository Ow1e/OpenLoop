import setuptools
import openloop

# Get requirements
with open("requirements.txt") as f:
    req = f.read().splitlines()

# Get markdown
with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="openloop",
 
    version=openloop.comb_code,
 
    author="Cyclone Communications",
 
    author_email="hello@cyclone.biz",
 
    description="OpenLoop package for extention.",

    long_description="""Library for extending OpenLoop, used by Cyclone Tools and OpenLite.""",
    long_description_content_type="text/markdown",
 
    url="",
    
    packages=["openloop"],
 
    install_requires=req,
 
    license="MIT",
 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)