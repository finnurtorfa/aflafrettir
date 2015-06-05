"""
Flask-Aflafrettir
-------------

A Flask extension that fetches landing information from the Directorate of
Fisheries (DOF) in Iceland's SOAP service and returns a sorted list of the
landings in an excel spreadsheet.
"""
from setuptools import setup


setup(
    name='Flask-Aflafrettir',
    version='0.2',
    url='https://github.com/finnurtorfa/aflafrettir',
    license='GPL',
    author='Finnur Torfason',
    author_email='finnurtorfa@gmail.com',
    description='DOF SOAP service extension',
    long_description=__doc__,
    py_modules=['flask_aflafrettir'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'suds-jurko',
        'openpyxl'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
