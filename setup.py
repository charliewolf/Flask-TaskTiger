from setuptools import setup

version = '0.0.1'

setup(
    name="Flask-TaskTiger",
    version=version,
    py_modules=["flask_tasktiger"],
    install_requires=['flask>=0.9', 'tasktiger'],
    author="Charlie Wolf",
    author_email="charlie@flow180.com",
    description="Flask TaskTiger",
    license="Tequilaware",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Utilities",
    ]
)
