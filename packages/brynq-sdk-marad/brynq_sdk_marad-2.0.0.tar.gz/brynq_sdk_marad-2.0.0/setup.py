from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_marad',
    version='2.0.0',
    description='Marad wrapper from BrynQ',
    long_description='Marad wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
    ],
    zip_safe=False,
)