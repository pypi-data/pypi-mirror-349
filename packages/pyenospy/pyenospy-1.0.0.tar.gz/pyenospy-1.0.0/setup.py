from setuptools import setup, find_packages

setup(
    name="pyenospy",
    version="1.0.0",
    author="enos",
    author_email="enos@enos.com",
    description="Basit ve kullanışlı bir mouse ve klavye kontrol kütüphanesi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyenospy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pywin32>=306",
    ],
) 
