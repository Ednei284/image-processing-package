from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="image_processing",
    version="0.1.0",
    project_urls={
        "Homepage": "https://github.com/Ednei284/image-processing-package",
        "Source": "https://github.com/Ednei284/image-processing-package",
    },
    author="Ednei",
    author_email="metal2024heavy@email.com",
    description="Uma breve descrição do seu pacote",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ednei284/image-processing-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy>=1.19.5", "scikit-image>=0.19.0", "matplotlib>=3.10.1"],
)
