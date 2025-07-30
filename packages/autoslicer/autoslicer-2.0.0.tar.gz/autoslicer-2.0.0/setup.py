from setuptools import setup, find_packages

setup(
    name="autoslicer",
    version="2.0.0",
    description="An automated tool for medical image processing with DICOM to NIfTI conversion, segmentation, and analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bruce Yang",
    author_email="bruceyang022059@gmail.com",
    url="",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "SimpleITK",
        "nibabel",
        "numpy",
        "torch",
        "totalsegmentator",
        "vtk"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)