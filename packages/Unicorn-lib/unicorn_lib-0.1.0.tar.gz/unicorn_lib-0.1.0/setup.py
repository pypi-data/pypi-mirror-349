from setuptools import setup, find_packages

# README.md を長い説明文として読み込むなら
long_description = open('README.md', encoding='utf-8').read()

setup(
    name='Unicorn_lib',              # PyPIに出す名前（ご自身のパッケージ名）
    version='0.1.0',                 # バージョン番号
    packages=find_packages(),        # 自動でパッケージディレクトリを探す
    install_requires=[],             # 依存ライブラリがあればリストに入れる
    author='あなたの名前',
    author_email='you@example.com',
    description='ログ出力付きテキスト操作ライブラリ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/あなたのGitHub/Unicorn_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
