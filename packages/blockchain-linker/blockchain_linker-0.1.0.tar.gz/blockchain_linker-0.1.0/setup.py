from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='blockchain_linker',
    version='0.1.0',
    description='사용자 정보를 블록체인으로 만들어주는 Python 패키지',
    author='lee-seokmin',
    author_email='dltjrals13@naver.com',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.7',
    url='https://github.com/lee-seokmin/blockchain_linker',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 