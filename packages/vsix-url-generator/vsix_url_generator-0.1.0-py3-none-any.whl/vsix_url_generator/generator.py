# -*- coding: utf-8 -*-
"""
@Auth ： dny
@Time ： 2025-05-22 9:15
"""


def generate_vsix_url(vsix_info: str) -> str:
    """
    Generate a VSIX file download URL from extension metadata.

    Args:
        vsix_info: A string containing the extension metadata with Identifier and Version.
                  Example:
                  '''
                  Identifier
                  eamodio.gitlens
                  Version
                  2025.5.2105
                  '''

    Returns:
        str: The complete VSIX download URL

    Raises:
        ValueError: If the input doesn't contain required fields
    """
    lines = [line.strip() for line in vsix_info.strip().split('\n') if line.strip()]

    try:
        identifier_index = lines.index("Identifier")
        version_index = lines.index("Version")

        publisher, name = lines[identifier_index + 1].split('.')
        version = lines[version_index + 1]

        return (
            f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/"
            f"{publisher}/vsextensions/{name}/{version}/vspackage"
        )
    except (ValueError, IndexError) as e:
        raise ValueError("Invalid VSIX info format. Must contain Identifier and Version fields.") from e