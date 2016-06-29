from setuptools import setup, find_packages
from os.path import join, dirname

setup(
        name='ftpscout',
        version=0.01,
        author='RubenRocha',
        author_email='rubenadsr96@gmail.com',
        url='https://github.com/RubenRocha/ftpscout',
        license=open(join(dirname(__file__), 'LICENSE')).read(),
        packages=find_packages(),
	py_modules=['ftpscout'],
        description='A multi-threaded Admin Finder.',
        long_description=open(join(dirname(__file__), 'README.md')).read(),
        classifiers=[
            'Programming Language :: Python :: 3.4',
            'License :: GPLv3',
            'Environment :: Console',
            'Topic :: Security',
            'Topic :: Utilities',
            'Development Status :: 5 - Production/Stable',
            ],
        entry_points={
            'console_scripts':
                ['ftpscout = ftpscout:main']
        }
    )
