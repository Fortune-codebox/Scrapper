from setuptools import setup

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().split('\n')
    print(requirements)

setup(
    name='mypackage',
    version='0.0.1',
    install_requires=requirements,
    entry_points={
         'console_scripts': [
            'wiki_scrapper = scrapping.main:default',
         ]
    }
)
