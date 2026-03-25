"""
Command-line entry point for the B24PySDK package.

This module allows the SDK version to be displayed when running:

    python -m b24pysdk
"""

from b24pysdk.version import SDK_NAME, SDK_VERSION


def main():
    """
    Print the installed SDK version.

    This function is executed when the package is run as a module.
    """
    print(f"{SDK_NAME} {SDK_VERSION}")


if __name__ == "__main__":
    main()
