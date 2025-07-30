from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        os.system("playwright install-deps")

from setuptools import setup, find_packages
setup(
    name="playwright-custom",
    version="0.2.0",
    description="Custom hook to install playwright deps",
    author="Your Name",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[
        "playwright"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    cmdclass={'install': CustomInstall},
)
