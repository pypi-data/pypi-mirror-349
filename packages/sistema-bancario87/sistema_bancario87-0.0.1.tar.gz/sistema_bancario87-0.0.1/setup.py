from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="sistema_bancario87",
    version="0.0.1",
    author="Matthew",
    author_email="87sans878798@gmail.com",
    description="Um projeto de teste para validar os meus conhecimentos adequeridos na plataforma da DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Matthew8717",
    packages=find_packages(),
    install_requirements=requirements,
    python_requires='>=3.9'
)
