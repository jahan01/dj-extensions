from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="dj-extensions",
    version="0.1.5post1",
    description="Yet another Django extension with set of generic reusable, pluggable mixins",
    long_description=readme(),
    keywords="django views mixins",
    author="Jahan Balasubramaniam",
    author_email="jahan.unofficial@gmail.com",
    url="https://github.com/jahan01/dj-extensions",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=['Django >= 1.7'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)