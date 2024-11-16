from api import BundledSubmission, get_session_key
from bundle import Bundle
import time
import sys


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: py main.py ../path/to/testcase/dir")
        return

    # Load our API key and authenticate

    with open("../.api_key", "r") as file:
        key = file.read()[:-1]

    session = get_session_key(key)

    # Bundle the image files from our test case directory into a request for analysis

    bundle = Bundle.from_dir(sys.argv[1])
    submission = BundledSubmission.from_bundle(bundle=bundle, session_key=session)
    submission.submit()

    # Check on our request; it takes a while :(
    while not submission.finished():
        print("Waiting for submission to solve...")
        time.sleep(10)

    # Submission is now finished
    latitude, longitude = submission.results()
    print(f"Latitude={latitude}, Longitude={longitude}")


if __name__ == "__main__":
    main()
