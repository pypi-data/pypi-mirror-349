import setuptools

setuptools.setup(
    url="https://q-chem.com/explore/qcloud",
    author_email="support@q-chem.com",
    description="CLI for interacting with Q-Cloud clusters",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['qcloud_user'],
    package_dir={'qcloud_user': 'src/qcloud_user'},
    license_files=["LICENSE.txt"],

    install_requires=[
        "boto3>=1.21.33",
        "botocore>=1.24.33",
        "demjson3>=3.0.6",
        "paramiko>=3.1.0",
        "pick>=2.2.0",
        "PyYAML>=5.3",
        "python-jose>=3.3.0",
        "pyopenssl>=22.1.0",
        "jose>=1.0",
        "Requests>=2.31.0",
    ],
    scripts=['src/qcloud_user/qcloud_user.py'],
)
