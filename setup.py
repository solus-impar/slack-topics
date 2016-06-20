import os.path
from setuptools import setup
from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

requirements_path = os.path.join(here, 'requirements.txt')
install_requirements = parse_requirements(requirements_path, session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='tb2k',
    version='0.1.0',
    description='A python3 slack topic bot.',
    author='Michael Canoy',
    author_email='canoym@students.wwu.edu',
    url='https://gitlab.cs.wwu.edu/canoym/tb2k',
    install_requires=requirements,
    license='MIT',
    keywords='topic bot Slack',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    py_modules=['tb2k'],
    entry_points={
        'console_scripts': [
            'tb2k=tb2k:main',
        ]
    },
)
