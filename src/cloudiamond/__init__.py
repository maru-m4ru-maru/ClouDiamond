"""ClouDiamond - Security toolkit for Scratch and TurboWarp."""

__version__ = "0.0.1"


class ClouDiamond:
    """Main ClouDiamond interface."""

    def __init__(self):
        self.version = __version__

    def info(self):
        return {
            "name": "ClouDiamond",
            "version": self.version,
            "status": "development",
        }


__all__ = ["ClouDiamond", "__version__"]
