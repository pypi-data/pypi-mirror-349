from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_leapsome',
    version='2.0.0',
    description='Leapsome wrapper from BrynQ',
    long_description='Leapsome wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'pandas>=2,<3',
        'openpyxl>=3,<4',
        'paramiko>=3,<4',
        'pysftp==0.2.9'
    ],
    zip_safe=False,
)
