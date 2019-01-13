from setuptools import setup

setup(
    name='drinklist_api',
    packages=['drinklist_api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_migrate',        
        'flask_cors',
    ],
)
