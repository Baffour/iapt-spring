#!/usr/bin/python

#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#  Thank you to Jon Romero for the idea for this module, as well as
#  Jonathan Lundell for the idea on integrating coverage.

"""
Web2py Test Runner
==================

About
-----

Runs all tests that exist in the ``tests`` directory. Up to one sub-level deep.

Your tests will be executed in a local environment, with access to everything
included in this file.

Create some tests and place them in the /<yourapp>/<tests>/<filename>.py

Follow the standard ``unittest.TestCase`` class unit tests.

Your tests will be responsible for creating their own fresh environment
of web2py. They have two options for doing this.

1. Create a fake environment, execute the models and controller manually.
2. Use webtest, and hook into web2py's ``wsgibase``.

Refer to the official documentation for more details.
"""

import unittest
import glob
import fnmatch
import sys
import os
import doctest
import cStringIO
from copy import copy

try:
    from webtest import TestApp
    _WEBTEST = True
except ImportError:
    _WEBTEST = False

try:
    import nose
    from nose.tools import *
    _NOSE = True
except ImportError:
    _NOSE = False

try:
    from coverage import coverage
    _COVER = True
except ImportError:
    _COVER = False

try:
    import gluon
    _GLUON = True
except ImportError:
    _GLUON = False

_TEST_APP_KEY = '<super random secret key here>'
_PATH = '/path/to/web2py'
_APP_PATH = '/path/to/web2py/applications/appname'

def set_args(env, *args):
    """
    Sets the environment args
    """
    for a in args:
        env['request']['args'].append(a)

def set_vars(env, type="post", **vars):
    """
    Sets the environment vars
    """
    rv = env['request'].vars
    rvt = env['request'][type+"_vars"]
    
    rv.update(vars)
    rvt.update(vars)

def set_crudform(tablename, fields, request, action="create", record_id=None):
    """
    Creates the appropriate request vars for forms

    set_crudform("bla", {"body": "yes"}, request, action="create", record_id=None)
    """
    for field_name in fields:
        request.vars[field_name] = fields[field_name]

    if action == "create":
        request.vars["_formname"] = tablename + "_" + action
    elif action == "update":
        request.vars["_formname"] = tablename + "_" + str(record_id)
        request.vars["id"] = record_id
    elif action == "delete":
        request.vars["_formname"] = tablename + "_" + str(record_id)
        request.vars["id"] = record_id
        request.vars["delete_this_record"] = True
    else:
        raise Exception("The form action '", action, "' does not exist")

def webtest():
    if not _WEBTEST:
        raise ImportError("""
You must have paste.WebTest package installed.

You may get the package by ``pip install webtest``.""")

    try:
        from gluon.main import wsgibase
    except ImportError:
        raise ImportError("""
No module named `gluon`, unable to find `wsgibase`

Make sure that you have executed the ``run`` function.

Make sure you have the correct URI that is the main web2py directory.

This should include your `applications` and `gluon` directories.""")

    app = TestApp(wsgibase, extra_environ=dict(
                TEST_APP=_TEST_APP_KEY,
                TEST_METHOD="WebTest",
    ))

    return app

def new_env(app='init', controller=None):
    try:
        from gluon import shell
    except ImportError:
        raise ImportError("""
No module named `gluon`, unable to find `shell`

Make sure you have the correct URI that is the main web2py directory.

This should include your `applications` and `gluon` directories.""")

    dir = os.path.join(_PATH, 'applications', app)

    _env = shell.env(app,
                    c=controller,
                    import_models=True,
                    dir=dir,
                    extra_request = {
                            'wsgi': {'environ': {
                                'TEST_APP': _TEST_APP_KEY,
                                'TEST_METHOD': 'FakeEnv'
                            }}
                        }
                    )

    if controller:
       execfile(os.path.join(dir, 'controllers', controller + '.py'), _env)

    return _env

def copy_db(env, db_name='db', db_link='sqlite:memory:'):
    try:
        from gluon.sql import DAL
    except ImportError:
        raise ImportError("""
No module named `gluon`, unable to find `sql.DAL`

Make sure you have the correct URI that is the main web2py directory.

This should include your `applications` and `gluon` directories.""")
    test_db = DAL(db_link)

    for tablename in env[db_name].tables:
        table_copy = [copy(f) for f in env[db_name][tablename]]
        test_db.define_table(tablename, *table_copy, migrate=True)

    return test_db

def setup(app, controller, db_name='db', db_link='sqlite:memory:'):
    env = new_env(app=app, controller=controller)
    db = copy_db(env, db_name, db_link)
    return env, db

def get_suite(app='init'):
    #apppath = os.path.join(_PATH, 'applications', app)

    suite = unittest.TestSuite()

    # Get all files with tests
    test_files = glob.glob(_APP_PATH + '/tests/*.py')
    test_files.extend(glob.glob(_APP_PATH + '/tests/*/*.py'))
    doc_test_files = glob.glob(_APP_PATH + '/controllers/*.py')


    if not test_files:
        raise Exception("No files found for app: %s" % _APP_PATH)

    # Unit Testing
    for test_file in test_files:
        if test_file.find('/'+os.path.basename(__file__)) != -1:
            continue
        g = copy(globals())

        # Execute our test file.
        execfile(test_file, g)

        # We will let the test execute its own environment

        # Add test.
        for key in g:
            if isinstance(g[key], type(unittest.TestCase)):
                suite.addTests(unittest.makeSuite(g[key]))

    for f in  doc_test_files:
        g = copy(globals())
        g.update(new_env(app, f[:-3]))
        execfile(f, g)
        suite.addTest(doctest.DocFileSuite(f, globs=g,
                module_relative=False))

    return suite

def run(path                = None,
        app                 = 'welcome',
        test_key            = 'secret',
        test_options        = {'verbosity': 1},
        test_report         = None,
        coverage_report     = None,
        coverage_exclude    = None,
        coverage_include    = None,
        DO_COVER            = True,
        DO_NOSE             = True,
        ):
    """
    Run all tests in ``path`` for ``app``. It will automatically exclude
    this tester file, gluon, '/usr', 'app/languages', 'app/tests', 'app/docs',
    'app/private'.

    .. note::

        If the current working directory is the path to web2py you do not
        need to specify path, you may leave it None.

        If you are in the web2py directory is determined by the ability to
        ``import gluon``.

    Keyword Arguments:

    path -- The path to the web2py directory.
    app -- Name of application to test.
    test_key -- Secret key to inject into the WSGI environment
    test_options -- Dictionary of options to pass along to the test runner
                    This is gets passed to either Nosetests or TextTestRunner
                    depending on what is available.

                    IE: {'verbosity': 3}

    test_report -- Path to a file, all output will be redirected here.
                   This redirects sys.stdout and sys.stderr to this file.
    coverage_report -- If ``test_report`` is none, this will print the coverage
                       report to this file, if coverage is installed.
    coverage_exclude -- List of omit_prefixes. If a filepath starts with this
                        value it will be omitted from the report
    coverage_include -- List of files to include in the report.
    DO_COVER -- If False, will disable coverage even if it is installed
    DO_NOSE -- If False, will use unittest.TestTextRunner, even if nosetests is
               is installed.
    """
    if test_report:
        print "Redirecting output to: ", test_report

        _STDOUT = sys.stdout
        _STDERR = sys.stderr
        _TR = open(test_report, 'w')
        sys.stdout = _TR
        sys.stderr = _TR

    print "The following modules are available"
    print "WebTest:     ", _WEBTEST
    print "NoseTest:    ", _NOSE
    print "Coverage:    ", _COVER

    # Set our globals
    global _PATH
    global _APP_PATH
    global _TEST_APP_KEY

    if _GLUON and not path:
        path = os.getcwd()

    _PATH           = path
    _APP_PATH       = os.path.join(_PATH, 'applications', app)
    _TEST_APP_KEY   = test_key

    # We need to make sure gluon is accessible, since it expects to be in the
    # root folder.    
    if not _GLUON:
        sys.path.append(_PATH)
        os.chdir(_PATH)

    # Get a suite of tests for app.
    suite = get_suite(app=app)

    if _COVER and DO_COVER:
        cov = coverage()
        cov.start()

    if _NOSE and DO_NOSE:
        nose.core.run(
            suite = suite,
            config = nose.config.Config(**test_options))
    else:
        unittest.TextTestRunner(**test_options).run(suite)

    if _COVER and DO_COVER:
        cov.stop()

        # Try to open a file, otherwise
        # use stringio.
        if isinstance(coverage_report, str) and not test_report:
            rpt = open(coverage_report, 'w')
            STRINGIO = False
        else:
            rpt = cStringIO.StringIO()
            STRINGIO = True

        # We want to omit these from the report.
        omit = ['gluon', '/usr', os.path.abspath(__file__)]
        
        # Ignore these folders.
        folders_to_omit = ['languages', 'tests', 'docs', 'private']
        for f in folders_to_omit:
            omit.append(os.path.join('applications', app, f))

        # Add any custom omissions
        if isinstance(coverage_exclude, (tuple, list)):
            omit.extend(coverage_exclude)

        # Now we need to get every python file that could
        # possibly be reported on. This way we only report 
        # python files that exist in our app.

        # I don't think we are interested in coverage of external
        # modules, they should have their own tests anyways.

        report_on = []
        for root, dirnames, filenames in os.walk(_APP_PATH):
            for filename in fnmatch.filter(filenames, '*.py'):
                report_on.append(os.path.join(root, filename))

        if isinstance(coverage_include, (tuple, list)):
            report_on.extend(coverage_include)

        # Do the report.
        cov.report(morfs = report_on, file = rpt, omit_prefixes = omit)

        # If we arn't saving the report to a file
        # go ahead and print it out.
        if STRINGIO:
            print rpt.getvalue()
