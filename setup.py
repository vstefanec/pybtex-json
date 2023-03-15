from setuptools import setup

setup(
    name='Pybtex JSON plugin',
    version='0.0.1',
    author='Vanja Štefanec',
    py_modules=['pybtex_json'],
    entry_points={
        'pybtex.database.output': 'json = pybtex_json:JSONWriter',
        'pybtex.database.output.suffixes': '.json = pybtex_json:JSONWriter',
    },
    install_requires=['pybtex']
)
