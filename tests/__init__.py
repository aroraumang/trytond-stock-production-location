# -*- coding: utf-8 -*-
"""
    tests/__init__.py

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import doctest
import unittest

import trytond.tests.test_tryton
from trytond import backend
from trytond.tests.test_tryton import DB_NAME

from tests.test_views_depends import TestViewsDepends


def doctest_dropdb(test):
    '''
    Remove database before testing
    '''
    Database = backend.get("Database")

    database = Database().connect()
    cursor = database.cursor(autocommit=True)
    try:
        database.drop(cursor, DB_NAME)
        cursor.commit()
    finally:
        cursor.close()


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests([
        unittest.TestLoader().loadTestsFromTestCase(TestViewsDepends),
    ])
    if DB_NAME == ':memory:':
        flags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.IGNORE_EXCEPTION_DETAIL     # noqa
        test_suite.addTests([
            doctest.DocFileSuite(
                'scenario_stock_production_location.rst',
                setUp=doctest_dropdb,
                tearDown=doctest_dropdb,
                encoding='utf-8',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE),
        ])
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
