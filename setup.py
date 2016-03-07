from setuptools import setup, find_packages

setup(
    name='rittenhouse',
    version='0.1.0',
    url='https://github.com/mattupstate/nycpython-2016-03-10',
    author='Matt Wright',
    author_email='matt@nobien.net',
    description='Example aiohttp application',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any'
)
