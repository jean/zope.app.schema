##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Field Factory Tests

$Id: test_fieldfactory.py,v 1.5 2004/03/09 12:39:10 srichter Exp $
"""
import unittest

import zope.app.schema

from zope.app import zapi
from zope.component.exceptions import ComponentLookupError
from zope.component.interfaces import IFactory
from zope.app.tests.placelesssetup import PlacelessSetup
from zope.security.management import newSecurityManager, system_user
from zope.schema.interfaces import IField, IText
from zope.interface import Interface
from zope.configuration import xmlconfig

class IFoo(Interface): pass

class TestFieldFactory(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        super(TestFieldFactory, self).setUp()
        newSecurityManager(system_user)
        context = xmlconfig.file('tests/test_fieldfactory.zcml',
                                 zope.app.schema)

    def testRegisterFields(self):
        factory = zapi.getUtility(None, IFactory,
                                  'zope.schema._bootstrapfields.Text')
        self.assertEquals(factory.title, "Text Field")
        self.assertEquals(factory.description, "Text Field")

    def testGetFactoriesForIField(self):
        factories = zapi.getFactoriesFor(None, IField)
        self.assertEqual(len(factories), 3)

    def testGetFactoriesForIText(self):
        factories = zapi.getFactoriesFor(None, IText)
        self.assertEqual(len(factories), 2)

    def testGetFactoriesUnregistered(self):
        factories = zapi.getFactoriesFor(None, IFoo)
        self.assertEqual(len(factories), 0)


def test_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestFieldFactory))
    return suite


if __name__=='__main__':
    unittest.TextTestRunner().run(test_suite())
