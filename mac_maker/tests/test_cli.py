"""Test the OSX-Provisioner CLI."""

from typing import Optional
from unittest import mock

from click.testing import CliRunner
from parameterized import parameterized_class
from .. import cli as cli_module
from ..cli import cli
from .fixtures import fixtures_git

CLI_MODULE = cli_module.__name__


class CLITestHarness(fixtures_git.GitTestHarness):
  """Test Harness for CLI Commands."""

  def setUp(self) -> None:
    super().setUp()
    self.runner = CliRunner()


@parameterized_class(
    [
        {
            "branch": None,
            "args": ""
        }, {
            "branch": "develop",
            "args": " --branch=develop"
        }
    ]
)
@mock.patch(CLI_MODULE + ".Jobs")
class TestPrecheckGithub(CLITestHarness):
  """Test the `precheck` CLI command with github repositories."""

  args: str
  branch: Optional[str]

  def test_precheck_get(self, m_jobs: mock.Mock) -> None:

    instance = m_jobs.return_value

    self.runner.invoke(
        cli,
        args=f"precheck github {self.repository_http_url}{self.args}",
    )
    instance.get_precheck_content_from_github.assert_called_once_with(
        self.repository_http_url, self.branch
    )

  def test_precheck_call(self, m_jobs: mock.Mock) -> None:
    instance = m_jobs.return_value
    mock_data = "data"

    instance.get_precheck_content_from_github.return_value = mock_data

    self.runner.invoke(
        cli,
        args=f"precheck github {self.repository_http_url}{self.args}",
    )

    instance.precheck.assert_called_once_with(mock_data)


@mock.patch(CLI_MODULE + ".Jobs")
class TestPrecheckSpec(CLITestHarness):
  """Test the `precheck` CLI command with spec files."""

  def test_precheck_get(self, m_jobs: mock.Mock) -> None:

    instance = m_jobs.return_value
    mock_spec_file = "/non-existent/path"

    self.runner.invoke(
        cli,
        args=f"precheck spec {mock_spec_file}",
    )
    instance.get_precheck_content_from_spec.assert_called_once_with(
        mock_spec_file
    )

  def test_precheck_call(self, m_jobs: mock.Mock) -> None:
    instance = m_jobs.return_value
    mock_precheck_data = "data"
    mock_spec_file = "/non-existent/path"

    instance.get_precheck_content_from_spec.return_value = mock_precheck_data

    self.runner.invoke(
        cli,
        args=f"precheck spec {mock_spec_file}",
    )

    instance.precheck.assert_called_once_with(mock_precheck_data)


@parameterized_class(
    [
        {
            "branch": None,
            "args": ""
        }, {
            "branch": "develop",
            "args": " --branch=develop"
        }
    ]
)
@mock.patch(CLI_MODULE + ".Jobs")
class TestApplyGithub(CLITestHarness):
  """Test the `apply` CLI command with GitHub repositories."""

  args: str
  branch: Optional[str]

  def test_apply_create(self, m_jobs: mock.Mock) -> None:
    instance = m_jobs.return_value

    self.runner.invoke(
        cli,
        args=f"apply github {self.repository_http_url}{self.args}",
    )
    instance.create_state_from_github_spec.assert_called_once_with(
        self.repository_http_url, self.branch
    )

  def test_provision_call(self, m_jobs: mock.Mock) -> None:
    instance = m_jobs.return_value
    mock_data = "data"

    instance.create_state_from_github_spec.return_value = mock_data

    self.runner.invoke(
        cli,
        args=f"apply github {self.repository_http_url}{self.args}",
    )

    instance.provision.assert_called_once_with(mock_data)


@mock.patch(CLI_MODULE + ".Jobs")
class TestApplySpec(CLITestHarness):
  """Test the `apply` CLI command with spec files."""

  def test_apply_create(self, m_jobs: mock.Mock) -> None:
    instance = m_jobs.return_value
    mock_spec_file = "/non-existent/path"

    self.runner.invoke(
        cli,
        args=f"apply spec {mock_spec_file}",
    )
    instance.create_state_from_local_spec_file.assert_called_once_with(
        mock_spec_file
    )

  def test_provision_call(self, m_jobs: mock.Mock) -> None:
    instance = m_jobs.return_value
    mock_precheck_data = "data"
    mock_spec_file = "/non-existent/path"

    instance.create_state_from_local_spec_file.return_value = mock_precheck_data

    self.runner.invoke(
        cli,
        args=f"apply spec {mock_spec_file}",
    )

    instance.provision.assert_called_once_with(mock_precheck_data)


@mock.patch(CLI_MODULE + ".VersionCommand")
class TestVersion(CLITestHarness):
  """Test the `version` CLI command."""

  def test_precheck_call(self, m_command: mock.Mock) -> None:
    instance = m_command.return_value

    self.runner.invoke(
        cli,
        args="version",
    )

    instance.get_version.assert_called_once_with()


@mock.patch(CLI_MODULE + ".Logger")
@mock.patch(CLI_MODULE + ".Jobs")
class TestLoggerIsInitializedWithDebug(CLITestHarness):
  """Test the logger is initialized with debug."""

  def test_precheck_call(self, _: mock.Mock, m_log: mock.Mock) -> None:
    instance = m_log.return_value

    self.runner.invoke(
        cli,
        args="--debug version",
    )

    m_log.assert_called_once_with(debug=True)
    instance.setup.assert_called_once_with()


@mock.patch(CLI_MODULE + ".Logger")
@mock.patch(CLI_MODULE + ".Jobs")
class TestLoggerIsInitializedWithoutDebug(CLITestHarness):
  """Test the logger is initialized without debug."""

  def test_precheck_call(self, _: mock.Mock, m_log: mock.Mock) -> None:
    instance = m_log.return_value

    self.runner.invoke(
        cli,
        args="version",
    )

    m_log.assert_called_once_with(debug=False)
    instance.setup.assert_called_once_with()
