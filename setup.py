from setuptools import setup

setup(
    name='bottle-log',
    version='1.0.0',
    license='New BSD',
    py_modules=['bottle_log'],
    author='Lars Hansson',
    author_email='romabysen@gmail.com',
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
