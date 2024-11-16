import json
from dataclasses import dataclass
import datetime as dt
from typing import Self

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
        with open(filepath, "r") as file:
            return cls.from_json(file.read())

    def __str__(self) -> str:
        return f"P(timestamp={self.timestamp.isoformat()}, heading={self.heading})"
