from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pygments_gdscript",
    version="1.0.4",
    author="ZackeryRSmith",
    author_email="zackery.smith82307@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZackeryRSmith/pygments-gdscript",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'pygments.lexers': [
            'gdscript = pygments_gdscript.gdscript_lexer:GDScriptLexer',
        ],
    },
)
