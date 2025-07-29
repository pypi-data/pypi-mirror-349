from setuptools import setup, find_namespace_packages

setup(
    name='brynq_sdk_azure_service_bus',
    version='2.0.0',
    description='Azure Service Bus wrapper from BrynQ',
    long_description='Azure Service Bus wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=find_namespace_packages(include=['brynq_sdk*']),
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=4,<5',
        'pandas>=2,<3',
        'azure-servicebus>=7.12',
        'pandas>=1,<3'
    ],
    zip_safe=False,
)
