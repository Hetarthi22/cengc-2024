import json
from dataclasses import dataclass
import datetime as dt
from typing import Any, Self

# All dates are in 2024 as per competition specifications
YEAR: int = 2024


@dataclass
class Parameters:
    """
    Represents the parameters associated with a bundle of images.
    """

    timestamp: dt.datetime  # UTC time-stamp
    heading: int  # Heading in degrees

    @classmethod
    def from_json(cls, raw_str: str) -> Self:
        """Creates a parameter object from a JSON string."""
        data = json.loads(raw_str)
        return cls(
            heading=data["heading"],
            timestamp=dt.datetime(
                year=2024,
                month=data["date"]["month"],
                day=data["date"]["day"],
                hour=data["utc_time"]["hour"],
                minute=data["utc_time"]["minute"],
                tzinfo=dt.timezone.utc,
            ),
        )

    @classmethod
    def from_file(cls, filepath: str) -> Self:
        """Load a parameter object from its JSON file."""
        with open(filepath, "r") as file:
            return cls.from_json(file.read())

    def __str__(self) -> str:
        return f"P(timestamp={self.timestamp.isoformat()}, heading={self.heading})"


@dataclass
class Solution:
    """Represents a solution file's parameters."""

    latitude: float  # Latitude in degrees
    longitude: float  # Longitude in degrees
    heading: int  # Heading in degrees

    @classmethod
    def from_file(cls, filepath: str) -> Self:
        with open(filepath, "r") as file:
            data = file.read()
        return cls(0, 0, 0)  # TODO


@dataclass
class Bundle:
    """A bundle of the four directional images, their parameters and their solution."""

    params: Parameters
    solution: Solution
    port: str
    starboard: str
    stern: str
    bow: str

    @classmethod
    def from_dir(cls, dirpath: str) -> Self:
        """Creates a bundle from the data in a test case directory."""

        return cls(
            params=Parameters.from_file(f"{dirpath}/parameters.json"),
            solution=Solution.from_file(f"{dirpath}/solution.txt"),
            port=f"{dirpath}/Port.gif",  # type: ignore
            bow=f"{dirpath}/Bow.gif",  # type: ignore
            starboard=f"{dirpath}/Starboard.gif",  # type: ignore
            stern=f"{dirpath}/Stern.gif",  # type: ignore
        )

    def __str__(self) -> str:
        return f"B(params={self.params})"
