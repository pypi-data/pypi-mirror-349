"""Manages all Heroku-specific aspects of the deployment process."""

import sys, os, re, json, subprocess
from pathlib import Path
from itertools import takewhile

import toml

from flask_simple_deploy.utils import plugin_utils
from flask_simple_deploy.utils.plugin_utils import fsd_config
from flask_simple_deploy.utils.command_errors import (
    DSDCommandError,
)

from . import deploy_messages as platform_msgs


class PlatformDeployer:
    """Perform the initial deployment to Heroku.

    If --automate-all is used, carry out an actual deployment.
    If not, do all configuration work so the user only has to commit changes, and run
    `git push heroku main`.
    """

    def __init__(self):
        """Establishes connection to existing simple_deploy command object."""
        self.templates_path = Path(__file__).parent / "templates"

    # --- Public methods ---

    def deploy(self, *args, **options):
        print("\nConfiguring project for deployment to Heroku...")

        self._validate_platform()

        self._prep_automate_all()

        self._add_procfile()
        self._add_python_version()

        self._add_requirements()
        self._conclude_automate_all()
        self._show_success_message()


    # --- Helper methods for deploy() ---

    def _validate_platform(self):
        """Make sure the local environment and project supports deployment to Heroku.

        Returns:
            None

        Raises:
            DSDCommandError: If we find any reason deployment won't work.
        """
        self._check_cli_installed()
        self._check_cli_authenticated()

    def _prep_automate_all(self):
        """Do intial work for automating entire process.
        - Create a heroku app to deploy to.
        - Create a Heroku Postgres database.

        Sets:
            str: self.heroku_app_name

        Returns:
            None
        """
        if not fsd_config.automate_all:
            return
        if fsd_config.local_testing:
            self.heroku_app_name = "empty_local_testing_project"
            print(f"Local testing, project name: {self.heroku_app_name}")
            return

        # Create heroku app.
        print("  Running `heroku create`...")
        cmd = "heroku create --json"
        output_obj = plugin_utils.run_quick_command(cmd)
        print(output_obj)

        # Get name of app.
        output_json = json.loads(output_obj.stdout.decode())
        self.heroku_app_name = output_json["name"]

    def _add_requirements(self):
        """Add Heroku-specific requirements."""
        packages = ["gunicorn"]
        plugin_utils.add_packages(packages)

    def _set_env_vars(self):
        """Set Heroku-specific environment variables."""
        if dsd_config.unit_testing:
            return

        self._set_heroku_env_var()
        self._set_debug_env_var()
        self._set_secret_key_env_var()

    def _add_procfile(self):
        """Add Procfile to project."""
        proc_command = "web: gunicorn app:app\n"
        path = fsd_config.project_root / "Procfile"
        plugin_utils.add_file(path, proc_command)

    def _add_python_version(self):
        """Add .python-version to project."""
        version_spec = "3.13\n"
        path = fsd_config.project_root / ".python-version"
        plugin_utils.add_file(path, version_spec)

    def _conclude_automate_all(self):
        """Finish automating the push to Heroku."""
        if not fsd_config.automate_all:
            return

        plugin_utils.commit_changes()

        print("  Pushing to heroku...")


        # Get the current branch name.
        cmd = "git branch --show-current"
        output_obj = plugin_utils.run_quick_command(cmd)
        print(output_obj)
        self.current_branch = output_obj.stdout.decode().strip()

        if fsd_config.local_testing:
            print("Local testing, not pushing to Heroku.")
            return

        # Push current local branch to Heroku main branch.
        # DEV: Note that the output of `git push heroku` goes to stderr, not stdout.
        print(f"    Pushing branch {self.current_branch}...")
        if self.current_branch in ("main", "master"):
            cmd = f"git push heroku {self.current_branch}"
        else:
            cmd = f"git push heroku {self.current_branch}:main"
        plugin_utils.run_slow_command(cmd)

        # Open Heroku app, so it simply appears in user's browser.
        print("  Opening deployed app in a new browser tab...")
        cmd = "heroku open"
        output = plugin_utils.run_quick_command(cmd)
        print(output)

    def _show_success_message(self):
        """After a successful run, show a message about what to do next."""

        # DEV:
        # - Say something about DEBUG setting.
        #   - Should also consider setting DEBUG = False in the Heroku-specific
        #     settings.
        # - Mention that this script should not need to be run again, unless
        #   creating a new deployment.
        #   - Describe ongoing approach of commit, push, migrate. Lots to consider
        #     when doing this on production app with users, make sure you learn.

        if fsd_config.automate_all:
            # Show how to make future deployments.
            msg = platform_msgs.success_msg_automate_all(
                self.heroku_app_name, self.current_branch
            )
        else:
            # Show steps to finish the deployment process.
            msg = platform_msgs.success_msg(
                fsd_config.pkg_manager, self.heroku_app_name
            )

        print(msg)

    # --- Utility methods ---

    def _check_cli_installed(self):
        """Verify the Heroku CLI is installed on the user's system.

        Returns:
            None

        Raises:
            DSDCommandError: If CLI not installed.
        """
        cmd = "heroku --version"
        try:
            output_obj = plugin_utils.run_quick_command(cmd)
        except FileNotFoundError:
            # This generates a FileNotFoundError on Linux (Ubuntu) if CLI not installed.
            raise DSDCommandError(platform_msgs.cli_not_installed)

        print(output_obj)

        # The returncode for a successful command is 0, so anything truthy means the
        # command errored out.
        if output_obj.returncode:
            raise DSDCommandError(platform_msgs.cli_not_installed)

    def _check_cli_authenticated(self):
        """Verify the user has authenticated with the CLI.

        Returns:
            None

        Raises:
            DSDCommandError: If the user has not been authenticated.
        """
        cmd = "heroku auth:whoami"
        output_obj = plugin_utils.run_quick_command(cmd)
        print(output_obj)

        output_str = output_obj.stderr.decode()
        # I believe I've seen both of these messages when not logged in.
        if ("Error: Invalid credentials provided" in output_str) or (
            "Error: not logged in" in output_str
        ):
            raise DSDCommandError(platform_msgs.cli_not_authenticated)

    def _check_heroku_project_available(self):
        """Verify that a Heroku project is available to push to.

        Assume the user has already run `heroku create.`

        Returns:
            None

        Raises:
            DSDCommandError: If there's no app to push to.

        Sets:
            dict: self.apps_list
            str: self.heroku_app_name
        """
        if dsd_config.unit_testing:
            self.heroku_app_name = "sample-name-11894"
            return

        # automate-all does the work we're checking for here.
        if dsd_config.automate_all:
            return

        plugin_utils.write_output("  Looking for Heroku app to push to...")
        cmd = "heroku apps:info --json"
        output_obj = plugin_utils.run_quick_command(cmd)
        plugin_utils.write_output(output_obj)

        output_str = output_obj.stdout.decode()

        # If output_str is emtpy, there is no heroku app.
        if not output_str:
            raise DSDCommandError(platform_msgs.no_heroku_app_detected)

        # Parse output for app_name.
        self.apps_list = json.loads(output_str)
        app_dict = self.apps_list["app"]
        self.heroku_app_name = app_dict["name"]
        plugin_utils.write_output(f"    Found Heroku app: {self.heroku_app_name}")

    def _set_heroku_env_var(self):
        """Set a config var to indicate when we're in the Heroku environment.
        This is mostly used to modify settings for the deployed project.
        """
        plugin_utils.write_output("  Setting Heroku environment variable...")
        cmd = "heroku config:set ON_HEROKU=1"
        output = plugin_utils.run_quick_command(cmd)
        plugin_utils.write_output(output)
        plugin_utils.write_output("    Set ON_HEROKU=1.")
        plugin_utils.write_output(
            "    This is used to define Heroku-specific settings."
        )
