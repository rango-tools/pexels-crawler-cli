import setuptools

def read_requirements(path='./requirements.txt'):
    with open(path, encoding='utf-8', errors='ignore') as file:
        install_requires = file.readlines()

    return install_requires

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pexels_cli",
    version="0.1.0",
    author="Amirhossein Douzandeh",
    author_email="amirzenoozi72@gmail.com",
    description="A Simple CLI To Get Image With Specific Tag From Pexels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rango-tools/pexels-crawler-cli",
    packages=setuptools.find_packages(),
    install_requires=read_requirements(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
    entry_points ={
            'console_scripts': [
                'pexels = pexels_cli.pexels_cli:main'
            ]
        },
    keywords ='pexels crawler selenium python package image photo dataset cli search tools web',
)