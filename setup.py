import os.path
from setuptools import setup, find_packages
from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

requirements_path = os.path.join(here, 'requirements.txt')
install_requirements = parse_requirements(requirements_path, session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='slack-topics',
    version='0.7.2',
    description='A python slack bot for topics.',
    author='Mike Canoy',
    author_email='mike@mikecanoy.net',
    url='https://github.com/solus-impar/slack-topics',
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    keywords='topic bot slack',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    py_modules=['slack_topics', 'topics'],
    entry_points={
        'console_scripts': [
            'slack-topics=slack_topics.bot:main',
        ]
    },
)
