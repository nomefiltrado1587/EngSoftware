from setuptools import setup


setup(
    name='simplcom',
    version='0.1.0',
    py_modules=['simplcom'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'simplcom = simplcom:oi',
        ],
    },
)