from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_google_drive',
    version='2.0.0',
    description='Google Drive wrapper from BrynQ',
    long_description='Groogle Drive wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'google-api-python-client>=2,<3',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)