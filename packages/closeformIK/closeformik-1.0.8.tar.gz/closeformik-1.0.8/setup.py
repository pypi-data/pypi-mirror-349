from setuptools import setup, find_packages
import os

# 动态库文件路径
dynamic_libraries = [
    'closeformIK/CloseFormIK.cpython-39-x86_64-linux-gnu.so',
    'closeformIK/CloseFormIK.cp39-win_amd64.pyd'
]

# 确保动态库文件存在
for library in dynamic_libraries:
    if not os.path.exists(library):
        raise FileNotFoundError(f"Required dynamic library '{library}' not found. Please ensure it exists in the directory.")

setup(
    name='closeformIK',
    version='1.0.8',
    packages=find_packages(),
    include_package_data=True,  # 启用 MANIFEST.in
    package_data={
        'closeformIK': [
            'CloseFormIK.cpython-39-x86_64-linux-gnu.so',
            'CloseFormIK.cp39-win_amd64.pyd'
        ]
    },
    install_requires=[
        'numpy',
        'scipy',
    ],
    python_requires='>=3.9',
    description='robot6Ik Package with dynamic libraries for both Linux and Windows',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Frank',
    url='https://github.com/Frank/closeformIK',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)