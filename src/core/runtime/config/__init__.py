"""
Runtime configuration resources.

Provides helper functions to load configuration files shipped with the
package.

Public API:
- get_cursor_agent_coords: load default cursor agent coordinate mapping.
"""

from importlib.resources import files


def get_cursor_agent_coords() -> bytes:
    """Return the raw contents of ``cursor_agent_coords.json``.

    Returns
    -------
    bytes
        Raw bytes of the JSON configuration file.
    """
    return files(__package__).joinpath("cursor_agent_coords.json").read_bytes()


__all__ = ["get_cursor_agent_coords"]
