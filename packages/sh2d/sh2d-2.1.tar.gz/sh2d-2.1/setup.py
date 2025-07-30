import setuptools

setuptools.setup(
    name="sh2d",
    version="2.1",
    author="sh2d",
    author_email="xx@qq.com",
    description="",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=['werkzeug','requests','dnspython','paramiko','pymysql','xlrd==1.2.0','xlsxwriter','zmail','xlwt','openpyxl','python-docx','docxtpl','pycryptodome','ddddocr','ruamel.yaml','pyzipper','pywin32','xlwings','python-whois','pyttsx3','colorlog','pyyaml','loguru'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
