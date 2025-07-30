"""Manages all Heroku-specific aspects of the deployment process."""

import flask_simple_deploy

from fsd_heroku.platform_deployer import PlatformDeployer
from .plugin_config import PluginConfig


@flask_simple_deploy.hookimpl
def fsd_get_plugin_config():
    """Get platform-specific attributes needed by core."""
    plugin_config = PluginConfig()
    return plugin_config


@flask_simple_deploy.hookimpl
def fsd_deploy():
    """Carry out platform-specific deployment steps."""
    platform_deployer = PlatformDeployer()
    platform_deployer.deploy()
