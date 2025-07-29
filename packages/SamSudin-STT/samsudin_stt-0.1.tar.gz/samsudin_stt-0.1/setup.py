from setuptools import setup,find_packages

setup(
    name='SamSudin-STT',
    version='0.1',
    author='Md Samsudin Rain',
    author_email='hackerz9766@gmail.com',
    description='This is speech to text package created by Md Samsudi Rain',
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]