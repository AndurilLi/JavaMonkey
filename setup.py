'''
Created on May 13, 2014

@author: pli
'''
from setuptools import setup

setup(
        name = "JavaMonkey",
        version = "1.0",
        description = "A JavaMonkey package based on ChimpChat",
        author = "Anduril, Yue.L",
        author_email = "pli@mstr.apps-poc.com,yuliu@mstr.apps-poc.com",
        packages = ['JavaMonkey','Pillow'],
        zip_safe = False,
        include_package_data = True
      )