from bundle import Bundle
from dataclasses import dataclass
import requests
import json
import random
import time
from typing import Self, Optional

# The base URL for making API requests
API_URL: str = "http://nova.astrometry.net/api"


@dataclass
class Job:
    """Represents an analysis job that has been created on the remote API."""

    id: int

    def get_coordinates(self) -> Optional[tuple[float, float]]:
        """
        Gets the right ascension (longitude) and declination (latitude) from the API.
        Returns a tuple of (latitude, longitude).
        """
        response = requests.get(f"{API_URL}/jobs/{self.id}/calibration")
        if response.status_code != 200:
            raise requests.HTTPError(response.status_code)
        data = response.json()
        if data.get("ra") is None:
            return None
        return (data["dec"], data["ra"])

    def get_status(self) -> str:
        """Returns the status of the request."""
        response = requests.get(f"{API_URL}/jobs/{self.id}")
        if response.status_code != 200:
            raise requests.HTTPError(response.status_code)
        print(response.raw)
        data = response.json()
        return data["status"]


@dataclass
class Submission:
    """Represents an API submission to the API."""

    id: int  # The submission ID
    session_key: str  # Auth session
    job: Job  # Associated job

    def get_status(self) -> bool:
        response = requests.get(f"{API_URL}/submissions/{self.id}")
        if response.status_code != 200:
            raise requests.HTTPError(response.status_code)
        print(response.json())
        data = response.json()
        if len(data["job_calibrations"]) == 0:
            return False

        return len(data["job_calibrations"][0]) == 4

    def solving(self) -> bool:
        """Detects if the submission is still being solved."""
        return self.job.get_status() == "solving"

    def _package_file(self, name: str) -> tuple[dict, bytes]:
        """
        Packages an image file into the format for being sent as a request.
        Modified from the example API client implementation provided by the API docs.
        Cited: https://github.com/dstndstn/astrometry.net/blob/main/net/client/client.py#L71
        """

        with open(name, "rb") as file:
            data = file.read()

        boundary_key = "".join([random.choice("0123456789") for i in range(19)])
        boundary = f"==============={boundary_key}=="
        headers = {"Content-Type": f'multipart/form-data; boundary="{boundary}"'}
        parameters = {
            "publicly_visible": "y",
            "allow_modifications": "d",
            "session": self.session_key,
            "allow_commercial_use": "d",
            "use_sextractor": True,
            "parity": 0,  # Halves search time
        }

        data_pre = (
            f"--{boundary}\nContent-Type: text/plain\r\nMIME-Version: 1.0\r\n"
            + 'Content-disposition: form-data; name="request-json"\r\n'
            + f"\r\n{json.dumps(parameters)}\n--{boundary}\n"
            + "Content-Type: application/octet-stream\r\nMIME-Version: 1.0\r\n"
            + f'Content-disposition: form-data; name="file"; filename="{name}"\r\n\r\n'
        )
        data_post = f"\n--{boundary}--\n"
        data = data_pre.encode() + data + data_post.encode()

        return headers, data

    def submit(self, file: str) -> None:
        """Submit the file as a submission to the API to process."""
        headers, data = self._package_file(file)
        response = requests.post(url=f"{API_URL}/upload", headers=headers, data=data)
        if response.status_code != 200:
            raise requests.HTTPError(response.status_code)
        self.id = response.json()["subid"]

    def queued(self) -> bool:
        """Returns true if the submission is queued."""
        response = requests.get(url=f"{API_URL}/submissions/{self.id}")
        if response.status_code != 200:
            raise requests.HTTPError(response.status_code)

        data = response.json()
        print(data)

        if len(data["jobs"]) == 0 or data["jobs"][0] is None:
            return False

        self.job.id = response.json()["jobs"][0]
        return True

    @classmethod
    def blank(cls, session_key: str) -> Self:
        """Creates a blank submission which is populated once submitted."""
        return cls(session_key=session_key, id=0, job=Job(0))


@dataclass
class BundledSubmission:
    """A bundle of four image submissions representing a total set of images in a test case."""

    bundle: Bundle
    port: Submission
    stern: Submission
    starboard: Submission
    bow: Submission

    def submit(self) -> None:
        """Makes four submissions, one for each image."""
        self.port.submit(self.bundle.port)
        self.stern.submit(self.bundle.stern)
        self.starboard.submit(self.bundle.starboard)
        self.bow.submit(self.bundle.bow)

    @classmethod
    def from_bundle(cls, bundle: Bundle, session_key: str) -> Self:
        """Creates a bundled submission from an existing bundle."""
        return cls(
            bundle=bundle,
            port=Submission.blank(session_key),
            starboard=Submission.blank(session_key),
            stern=Submission.blank(session_key),
            bow=Submission.blank(session_key),
        )

    def queued(self) -> bool:
        """Detects if all submissions in the bundle are queued."""
        return self.port.queued() and self.stern.queued() and self.bow.queued() and self.starboard.queued()

    def finished(self) -> bool:
        """Detects if the submission bundle as a whole has finished."""

        if not self.queued():
            return False

        return (
            not self.port.solving()
            and not self.stern.solving()
            and not self.starboard.solving()
            and not self.bow.solving()
        )

    def results(self) -> tuple[float, float]:
        """Return latitude, longitude pair averaged from all the results."""
        lat = 0
        lon = 0
        count = 0

        coordinates = self.port.job.get_coordinates()
        if coordinates is not None:
            lat += coordinates[0]
            lon += coordinates[1]
            count += 1

        coordinates = self.stern.job.get_coordinates()
        if coordinates is not None:
            lat += coordinates[0]
            lon += coordinates[1]
            count += 1

        coordinates = self.bow.job.get_coordinates()
        if coordinates is not None:
            lat += coordinates[0]
            lon += coordinates[1]
            count += 1

        coordinates = self.starboard.job.get_coordinates()
        if coordinates is not None:
            lat += coordinates[0]
            lon += coordinates[1]
            count += 1

        # TODO: what if one of these has failed
        lat /= 4
        lon /= 4
        return (lat, lon)


def get_session_key(api_key: str) -> str:
    """Logs in and creates a session for the API."""
    response = requests.post(f"{API_URL}/login", data={"request-json": json.dumps({"apikey": api_key})})
    if response.status_code != 200:
        raise requests.HTTPError(response.status_code)
    print(response.json())
    return response.json()["session"]
