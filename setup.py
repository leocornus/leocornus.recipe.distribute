from setuptools import setup, find_packages
import os

version = '2.1.4'
name = 'leocornus.recipe.distribute'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name=name,
    version=version,
    description="zc.buildout recipe for package and distribute files, modules, libs, archives, etc.",
    long_description= (
      '`Check the GitHub Page <http://github.com/leocornus/%s>`_ for details document\n' % name 
      + '\n' +
      'General Usage\n'
      '*******************\n'
      + '\n' +
      read('leocornus','recipe','distribute','README.rst')
      + '\n' +
      'Download\n'
      '***************\n'
      ),
    classifiers=[
     'Framework :: Buildout',
     'Intended Audience :: Developers',
     'License :: OSI Approved :: GNU General Public License (GPL)',
     'Topic :: Software Development :: Build Tools',
     'Topic :: Software Development :: Libraries :: Python Modules',
      ],

    keywords='development buildout recipe package distribute',

    author='Sean Chen',
    author_email='sean.chen@leocorn.com',
    url='http://github.com/leocornus/%s' % name,
    license='GPLv2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['leocornus', 'leocornus.recipe'],
    include_package_data = True,

    zip_safe=False,
    install_requires = [
      'zc.buildout >= 1.4.0',
      'setuptools',],
    extras_require={
      'test' : ['zope.testing'],
    },
    tests_require = ['zope.testing'],
    test_suite = '%s.tests.testDoctests.test_suite' % name,

    entry_points = { 'zc.buildout' : ['default = leocornus.recipe.distribute:Dist',
                                      ] },
)
