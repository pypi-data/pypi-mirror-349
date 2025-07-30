# setup.py
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.md')

try:
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='Unicorn_lib',      # PyPIで登録したい名前
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Your Name',
    author_email='you@example.com',
    description='ログ出力付きのテキスト操作ライブラリ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/あなた/Unicorn_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
