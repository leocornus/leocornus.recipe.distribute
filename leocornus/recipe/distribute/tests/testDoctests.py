# testDoctests.py

from unittest import TestSuite 
from doctest import DocFileSuite
from doctest import ELLIPSIS
from doctest import NORMALIZE_WHITESPACE

from zc.buildout.testing import buildoutSetUp
from zc.buildout.testing import install_develop
from zc.buildout.testing import buildoutTearDown

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

optionflags = (ELLIPSIS | NORMALIZE_WHITESPACE)

# set up the buildout testing enviroment.
def setUp(test):

    buildoutSetUp(test)
    install_develop('leocornus.recipe.distribute', test)

def test_suite():

    suite = TestSuite()
    suite.addTest(
        DocFileSuite(
            'README.rst',
            package='leocornus.recipe.distribute',
            setUp=setUp,
            tearDown=buildoutTearDown,
            optionflags=optionflags,
            ),
        )

    suite.addTest(
        DocFileSuite(
            'tests/basicDataCompressAndArchiving.rst',
            package='leocornus.recipe.distribute',
            ),
        )

    # testing the version patterns.
    # try to find the version from a file, likely a README.txt
    suite.addTest(
        DocFileSuite(
            'tests/versionPatternGrep.rst',
            package='leocornus.recipe.distribute',
            ),
        )

    # hold this for now, we might not depend on fabric.
    #suite.addTest(
    #    DocFileSuite(
    #        'tests/basicLocalFabric.rst',
    #        package='leocornus.recipe.distribute',
    #        ),
    #    )

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
