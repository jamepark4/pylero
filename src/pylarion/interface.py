# TODO Erase this file after verifying that it is not needed for anything.
# It is part of original code and I am unsure of its purpose.

# # -*- coding: utf8 -*-
# from __future__ import absolute_import, division, print_function, unicode_literals
# 
# '''
# Pylarion: Python wrapper for Polarion.
# 
# This is not a general Polarion library. It assumes a specific environment:
# - Red Hat's Polarion configuration and implementation
# - BaseOS QE needs and conventions
# 
# It has two main components:
# 
# ------------------------------------------------------------------------------
# (1) CLI
# ------------------------------------------------------------------------------
# 
# Command line tools to interact with Polarion.
# 
# Sorry, just a placeholder, nothing here yet. In the end, it would be nice
# to have tools as complete, useful, and nice as:
# https://wiki.test.redhat.com/BaseOs/Projects/IntegrationScripts
# but..
# 
# ------------------------------------------------------------------------------
# (2) Library
# ------------------------------------------------------------------------------
# 
# The library to support the CLI. Moreover, it may be useful for occasional
# scripting or interactive sessions.
# 
# The library tries to be internally very simple:
# - no configuration
# - no data caching
# - no call caching (like multicalls in python-nitrate)
# - no "live" containers (like in python-nitrate)
# - no uniqueness management
# The public methods provided by this library usually translate to one
# or several immediate calls of the Polarion SOAP interface.
# 
# The expected way to work with data is:
# 1. Define a Server
# 2. Open a Session
# 3. a) Use the Session's method to find/create/delete objects, and
#    b) Use the objects' methods for actions not directly provided by
#       the Session
# 4. Close the Session (done automatically if you use
#    "with server.session()").
# 5. Back to 2 if you wish.
# 
# Data model:
# 
# 1. "SUDS" objects
# 
#    are used by the underlying SUDS. Their classes are created from WDSLs
#    on the go (from a living session) using so called factories. This library
#    does not define the classes, just uses them. In general, the SUDS objects
#    are used to pass data to/from Polarion's SOAP interface. They do not
#    provide much comfort to work.
# 
# 2. This library's own data objects ("front-end" objects)
# 
#    are objects created and maintained in this library. They are rough
#    counterparts to the SUDS objects above. The class hierarchy is:
# 
#    AbstractPolarionMappingObject
#      |
#      +- BasePolarion .. not Polarion persistent ("crates")
#      |    |
#      |    +- t.Text .. '*:Text' of all web services
#      |    |    |
#      |    |    + TrackerText        .. for Tracker web service
#      |    |    + TestManagementText .. for TestManagement web service
#      |    |
#      |    +- TestRecord  .. 'tns3:TestRecord' of the TestManagement
#      |                                                web service
#      |
#      +- AbstractPolarionPersistentObject .. persisted in Polarion
#           |
#           +- wi.WorkItem
#           |    |
#           |    +- AbstractTest
#           |         |
#           |         +- FunctionalTestCase
#           |         +- StructuralTestCase
#           |         +- NonFunctionalTestCase
#           |         +- TestSuite
#           |
#           +- Document
#           |    |
#           |    +- SimpleTestPlan .. see below
#           |
#           +- AbstractTestRun
#                |
#                +- SimpleTestRun .. see below
# 
#    Internally, these classes have conversion methods to/from their
#    respective SUDS counterparts.
# 
#    Objects of concrete classes under AbstractPolarionPersistentObject
#    define the basic CRUD (CREATE, RETRIEVE, UPDATE, DELETE) operations
#    on Polarion but they are not meant to be used directly. Instead, higher
#    level operations are defined either on the objects or on Session
#    (see below).
# 
#    Objects stored in Polarion are identified by the Polarion unique
#    identifier, "URI". In the library, the corresponding attribute is "puri".
#    However, the library does not provide any uniqueness management: You
#    can retrieve the same Polarion object into two independent library objects
#    (with the same "puri"), update them and store them independently; the last
#    update "wins" and persists.
# 
#    Test Cases are modeled by subclasses of AbstractTest. Their corresponding
#    Polarion's counterparts are Works Items of the same names and the following
#    mapping:
#    - Test Case's script_url = the first and only Work Item's hyperlink
#    - Test Case's automation = Work Item's custom field "caseautomation"
#    - Test Case's tags = Work Item's custom field "tcmstags"
#    (The mapping is provisional.)
# 
#    SimpleTestPlan and SimpleTestRun are the key data objects of this library
#    - they represent test plans and test runs as they are usually understood
#    by Base OS QE. Among others, test plans are hierarchically organized
#    and a test run can be linked to a test plan it performs.
# 
#    For the sake of easy prototyping (no custom fields for now), let's specify: 
# 
#    SimpleTestPlan
#      - is a Polarion Document
#      - type.id = "testspecification"
#      - its content (text) consists of three parts:
#        - whatever an user wants there, Pylarion will ignore this
#        - Pylarion-specific data, in YAML (surrounded by [..])
#          [pylarion.structured-field-start]
#          header:
#            subject: pylarion
#            formatVersion: 0.0
#            dataType: SimpleTestPlan
#          data:
#            parentPlan:
#              uri: subterra:data-service:objects:...
#          [pylarion.structured-field-end]
#        - list of *linked* work items (test cases)
# 
#    SimpleTestRun
#      - is a Polarion Test Run
#      - it's wiki contains, among others, a YAML (surrounded ..) text
#        as follows:
#        [pylarion.structured-field-start]
#        header:
#          subject: pylarion
#          version: 0.0
#          dataType: SimpleTestRun
#        data:
#          plan:
#            uri: subterra:data-service:objects:...
#          automation:
#            beaker:
#              jobs: [TJ#774928, TJ#774925, TJ#774923, TJ#775986]
#              matrix: https://beaker.engineering.redhat.com/..
#              ..
#        [pylarion.structured-field-start]
# 
# 3. Service objects
# 
#    are just runtime overhead. The following classes are important:
# 
#    - PylarionLibException and its subclasses may be raised by this library
# 
#    - Server
#      - a container for data needed to connect to a Polarion instance
#      - provides Sessions
# 
#    - Session
#      - wraps low level Polarion sessions
#      - mediates transactions (as provided by Polarion)
#      - it is the entry point to work with data
# '''
# 
# # Maybe there's a better way to declare an interface in Python (the abc
# # module?). For now just stick with blissful ignorance.
# 
# if False:
# 
#     class PylarionLibException(Exception): pass
# 
#     class AbstractPolarionMappingObject:
#         def  __init__(self, session): pass
# 
#         def _copy(self, another): pass
# 
#         def _fill_missing_values(self, project=None, namespace=None): pass # defaults where not set 
# 
#         # --------------------------------------------------------------------
#         # Conversions
#         #
#         # As in any real world code, the library often needs to convert between
#         # front-end objects (the library works with) and back-end object (here,
#         # the SUDS object). Let's have uniform names for the conversions. All
#         # conversion are meant to be internal to the library.
# 
#         # Is a given SUDS object convertible to the current "front-end" class?
#         @classmethod
#         def _is_convertible(cls, suds_object): pass
# 
#         # Create a front-end object from a SUDS object. Make the new instance
#         # as much specific as possible. In other words, create an instance of
#         # the current class or, if possible, its most specific subclass.
#         @classmethod
#         def _map_from_suds(cls, session, suds_object): pass
# 
#         # Convert a front-end object to SUDS. Use all available data ("go to
#         # subclasses")
#         def _map_to_suds(self): pass
# 
#         # Convert data specific just for the current level of abstraction and
#         # above. (Helper methods to implement the conversions above.)
#         @classmethod
#         def _map_specific_attributes_to_suds(cls, abstract_polarion_mapping_object, suds_object): pass
#         @classmethod
#         def _map_specific_attributes_from_suds(cls, suds_object, abstract_polarion_mapping_object): pass
# 
#         # End of Conversions
#         # --------------------------------------------------------------------
# 
# 
#     # Parent class for "not-directly-persisted" data
#     class BasePolarion(AbstractPolarionMappingObject): pass
# 
#     # Tracker Web Service's 'tns2:Text'
#     class TrackerText(bp.BasePolarion): pass
# 
#     # TestManagement Web Service's 'tns3:TestRecord'
#     class TestRecord(bp.BasePolarion): pass
# 
#     # Parent class for "directly-persisted" data
#     class AbstractPolarionPersistentObject(AbstractPolarionMappingObject):
#         # identification: puri = Polarion URI
#         def _crud_create(self, project=None): pass
#         def _crud_retrieve(self): pass  # by URI
#         def _crud_update(self): pass
#         def _crud_delete(self): pass
# 
#     class wi.WorkItem(AbstractPolarionPersistentObject): pass
# 
#     # Parent class for tests
#     class AbstractTest(WorkItem): pass
# 
#     class FunctionalTestCase(AbstractTest): pass
#     class StructuralTestCase(AbstractTest): pass
#     class NonFunctionalTestCase(AbstractTest): pass
#     class TestSuite(AbstractTest): pass
# 
#     class Document(AbstractPolarionPersistentObject):
#         def __init__(self, namespace=None): pass
# 
#     # Pylarion-friendly test plan (see above)
#     class SimpleTestPlan(Document):
#         def get_children_plans(self, project=None, all_projects=False): pass
#         def create_child_plan(self, project=None): pass
#         def get_test_cases(self, project=None, all_projects=False): pass
#         def add_test_case(self, testCase): pass
#         def delete_test_case(self, arg): pass  # TestCase instance, URI, test "name" like "/CoreOS/.."
#         def create_run(self, project=None): pass
# 
#     class AbstractTestRun(AbstractPolarionPersistentObject): pass
# 
#     # Pylarion-friendly test run (see above)
#     class SimpleTestRun(AbstractTestRun):
#         def get_test_plan(self): pass
#         def get_test_records(self): pass
#         def delete_test_record(self, test_ref): pass  # TestRecord or TestCase instance, TestCase URI, test "name"
#         def set_test_recordResult(self, test_ref, result, duration=None, executed=None, comment=None): pass
# 
#     class Server:
#         # no singleton dance
# 
#         def __init__(self, url, login, password, default_project=None, default_namespace=None, timeout=60): pass
#         def session(self): pass  # a context manager to enter/exit a session
# 
#     class Session:
# 
#         def tx_begin(self): pass
#         def tx_commit(self): pass
#         def tx_rollback(self): pass
#         def tx_release(self): pass  # if in a session: rollback
#         def transaction(self): pass  # a context manager for a "normal" transaction
# 
#         # For all AbstractPolarionPersistentObject subclasses XXX:
#         def newXXX(self, project=None, namespace=None): pass
#         def getXXXByPID(self, pid, project=None): pass
#         def getXXXByPURI(self, puri): pass
#         def findAllXXXs(self, query, project=None, all_projects=False, namespace=None): pass
#         def findXXXsByQuery(self, query, project=None, all_projects=False, namespace=None): pass
#         def findXXXsByTCMSTag(self, tag, project=None, all_projects=False): pass  # just for tests cases
#         def loadXXX(self, reference, project=None, namespace=None): pass  # URI or ID or "title" or ..
#         def save(self, obj): pass  # CRUD create or update
#         def delete(self, obj): pass  # CRUD delete
#         # Notes
#         # - other manipulations: via public methods on the persisted objects
#         # - get* and find* return as concrete instances as possible
#         # - namespace= makes sense just for Documents
# 
# 
#     # ------------------------------------------------------------------------
#     # Examples
#     # ------------------------------------------------------------------------
# 
#     def _demoCode0001():
#         '''
#         Create a test run from selected test cases of a test plan.
# 
#         No explicit transaction handling (each background operation with
#         Polarion runs in its own implicit transaction). As a consequence,
#         just a partial state can be recorded in the end.
#         '''
#         with Server(url='http://example.com/polarion', login='joe', password='secret_password', default_project='BaseOS') as s:
#             generalPlan = s.loadSimpleTestPlan('DTS 3.0 General test plan')
#             runForEclipse = generalPlan.create_run()
#             runForEclipse.description = 'DTS 3.0 Beta 2: Eclipse'
#             s.save(runForEclipse)
#             for testCase in runForEclipse.get_test_records():
#                 if 'eclipse' not in testCase.tags:
#                     runForEclipse.delete_test_record(testCase)
# 
#     def _demoCode0002():
#         '''
#         Create a test case, a plan, a run, perform, and delete the run.
# 
#         Create a new test case. Create a new test plan derived from a general
#         plan. Add the new test case to the new plan. Create a new run from
#         the new plan. Records results in the run. Delete the run.
# 
#         The whole procedure runs in a transaction: If no exception happens
#         then the data stay recorded in Polarion (the new test case and the
#         new plan will be permanent). In case of an exception an automatic
#         rollback will take place.
#         '''
#         with Server(url='http://example.com/polarion', login='joe', password='secret_password', default_project='JoesProject') as s:
#             with s.transaction():
# 
#                 # create a new functional test case
#                 myNewTest = s.new_functional_test_case()
#                 myNewTest.title = '/CoreOS/systemd/Regression/bz855313-journald-truncates-messages-after-LF'
#                 myNewTest.description = "Verify bz855313's fix. Send messages with line feeds and see if they get recorded"
#                 myNewTest.initial_estimate = '10m'
#                 myNewTest.script_url = 'http://pkgs.devel.redhat.com/cgit/tests/eclipse/tree/BaseOS/systemd/Regression/bz855313-journald-truncates-messages-after-LF'
#                 myNewTest.automation = 'Automated'
#                 s.save(myNewTest)
# 
#                 # create a test plan
#                 myGeneralPlan = s.loadSimpleTestPlan('XYZP-0007')
#                 myNewSpecializedPlan = myGeneralPlan.create_child_plan()
#                 myNewSpecializedPlan.add_test_case(myNewTest)
# 
#                 # create a test run
#                 myNewRun = myNewSpecializedPlan.create_run()
#                 myNewRun.setNotes('Arbitrary notes, f.ex. refer to a Beaker task')
#                 for test_record in myNewRun.get_test_records():
#                     myNewRun.set_test_recordResult(test_record, 'passed', comment='beaker-task = https://beaker.engineering.redhat.com/tasks/executed?recipe_task_id=..')
# 
#                 # but let it go
#                 s.delete(myNewRun)