from time import time
import setuptools
# c:\Python38\python.exe setup.py clean --all
# c:\Python38\python.exe setup.py sdist
# c:\Python38\python.exe -m build
# c:\Python38\python.exe -m twine upload dist/* --skip-existing
# 用户名 jerry1979
# pypi-AgEIcHlwaS5vcmcCJDExZGUyMjE3LTBlNGQtNGYzMC05NDlkLTcwNzVhMjM3YzFiYwACKlszLCIzNWQzNjY4My0xMTllLTQ1MGItYjcxOC01ODEyNzM5YWRhYTAiXQAABiCSEWB_uQmMjWo8LWkScnqm1BRgTKlUqawEN2y6Yz0Lag

'''
d1815a30159a81fd
691362c6f6f71b38
a9a1df09e6cf5c22
3b09f1a0d8f6c52a
4d52b7b60c6d15ae
3e4f93aada7a3901
5b95b9ab769f9e58
72097631bef24c76
'''

# (myBase) E:\BaiduSyncdisk\pyLib\mxupyPackage>python setup.py sdist bdist_wheel

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxupy",
    version="1.0.7",
    author="jerry",
    author_email="6018421@qq.com",
    description="An many/more extension/utils for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "mxupy"},
    packages=setuptools.find_packages(where="mxupy"),
    python_requires=">=3.8",
)
