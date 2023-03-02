"""
This module provides fixtures for test setup.
You can use these fixtures for all tests in your suite.
You could also copy-paste this module into your own test project to provide Applitools setup for your tests.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import os
import pytest

from applitools.playwright import *
from playwright.sync_api import Page


# --------------------------------------------------------------------------------
# Session-Scope Fixtures
#   These fixtures run one time for the whole test suite.
#   Subsequent calls use the value cached from the first execution.
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def api_key():
  """
  Reads the Applitools API key from an environment variable.
  """
  return os.getenv('APPLITOOLS_API_KEY')


@pytest.fixture(scope='session')
def runner():
  """
  Creates the classic runner.
  After the test suite finishes execution, closes the batch and report visual differences to the console.
  Note that it forces pytest to wait synchronously for all visual checkpoints to complete.
  """
  run = ClassicRunner()
  yield run
  print(run.get_all_test_results())


@pytest.fixture(scope='session')
def batch_info():
  """
  Creates a new batch for tests.
  A batch is the collection of visual checkpoints for a test suite.
  Batches are displayed in the Eyes Test Manager, so use meaningful names.
  """
  return BatchInfo("Example: Playwright Python with the Classic runner")


@pytest.fixture(scope='session')
def configuration(api_key: str, batch_info: BatchInfo):
  """
  Creates a configuration for Applitools Eyes to test 3 desktop browsers and 2 mobile devices.
  """

  # Construct the object
  config = Configuration()

  # Set the batch for the config.
  config.set_batch(batch_info)

  # Set the Applitools API key so test results are uploaded to your account.
  # If you don't explicitly set the API key with this call,
  # then the SDK will automatically read the `APPLITOOLS_API_KEY` environment variable to fetch it.
  config.set_api_key(api_key)

  # Return the configuration object
  return config


# --------------------------------------------------------------------------------
# Function-Scope Fixtures
#   These fixtures run one time before each test that calls them.
#   Returned values are not cached and reused across different tests.
# --------------------------------------------------------------------------------

@pytest.fixture(scope='function')
def eyes(
  runner: ClassicRunner,
  configuration: Configuration,
  page: Page,
  request: pytest.FixtureRequest):
  """
  Creates the Applitools Eyes object connected to the ClassicRunner and set its configuration.
  Then, opens Eyes to start visual testing before the test, and closes Eyes at the end of the test.
  
  Opening Eyes requires 4 arguments:
    1. The Playwright Page object to "watch".
    2. The name of the application under test.
       All tests for the same app should share the same app name.
       Set this name wisely: Applitools features rely on a shared app name across tests.
    3. The name of the test case for the given application.
       Additional unique characteristics of the test may also be specified as part of the test name,
       such as localization information ("Home Page - EN") or different user permissions ("Login by admin").
    4. The viewport size for the local browser.
       Eyes will resize the web browser to match the requested viewport size.
       This parameter is optional but encouraged in order to produce consistent results.
  """

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)

  eyes.open(
    driver=page,
    app_name='ACME Bank Web App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1024, 768))
  
  yield eyes
  eyes.close_async()
