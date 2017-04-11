from setuptools import setup


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


setup(
    name='bottle-log',
    version='1.0.0',
    license='New BSD',
    py_modules=['bottle_log'],
    description='Improved logging for Bottle.',
    long_description=read('README.rst'),
    author='Lars Hansson',
    author_email='romabysen@gmail.com',
    url='https://github.com/romabysen/bottle-log',
    install_requires=[
        'bottle>=0.10.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Bottle',
        'License :: OSI Approved :: BSD License'
    ]
)
