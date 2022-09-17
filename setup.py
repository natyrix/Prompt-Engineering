from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req:
    req_list = req.readlines()
    req_list = [sd.replace('\n', '') for sd in req_list]

requirements = req_list
test_requirements = ['pytest>=3']

setup(
    requires=requirements,
    author="Natnel Melese",
    email="natrix277@gmail.com",
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Prompt Engineering",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='scripts',
    name='scripts',
    packages=find_packages(include=['scripts', 'scripts.*',
                                    'data','staticFiles','templates',
                                    'tests', 'notebooks','logs', 'dvc-storage']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/natyrix/Prompt-Engineering',
    version='1.0.0',
    zip_safe=False,
)