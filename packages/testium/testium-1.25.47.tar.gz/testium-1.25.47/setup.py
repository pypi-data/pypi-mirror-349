from setuptools import setup, find_packages

setup(
    name='testium',
    version='1.25.47',
    url='https://gitlab.wrccorp.cn/AutoTesting/testium.git',
    license='©2009-2024 wrc All Rights Reserved',
    author='wrc',
    author_email='a18786478486@163.com',
    packages=find_packages(),
    install_requires=[
        # 'Appium-Python-Client>=1.3.0',
        'selenium==4.12.0',
        'pytest>=5.2.2',
        # 'pyautogui',
        # 'aiocontextvars',
        'retry>=0.9.2',
        # 'sre_yield',
        'Pillow==10.1.0',
        'Appium-Python-Client==3.1.0',
        'loguru>=0.5.0',
        # 'selenium>=4.1.0',
        'jsonpath==0.82.2',
        'requests>=2.23.0',
        'urllib3==1.26.15', ])
