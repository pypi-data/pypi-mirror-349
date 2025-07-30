import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="sit-timeline-logging",
    version="0.0.2",
    author="anusorn.l",
    author_email="nusorn.l@somapait.com",
    description="SIT timeline logging package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],
 )