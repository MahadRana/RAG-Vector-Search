from setuptools import find_packages, setup

HYPHEN_E_DOT = '-e .'
def get_requirements(filename):
    requirements = []
    with open(filename) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
             requirements.remove(HYPHEN_E_DOT)
        return requirements

setup(
    name='RAG_Project',
    version='0.0.1',
    author='Mahad',
    author_email='mahadmrana@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
) 