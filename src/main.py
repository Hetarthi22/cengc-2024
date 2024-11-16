from api import BundledSubmission, get_session_key
from bundle import Bundle
import time
import sys


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: py main.py ../path/to/testcase/dir")
        return

    # Load our API key and authenticate
    # Yes, I know this API key should not be in the code. However, I am trying to make running the demo as simple as
    # possible for the programming director. This avoids him having to create a file and put the API key in it, and me
    # finding a way to give him my API key. I will absolutely be changing my API key following this competition (and
    # actually, deleting my account on the website).
    key = "xfgiixgqacwkoabs"
    session = get_session_key(key)

    # Bundle the image files from our test case directory into a request for analysis

    bundle = Bundle.from_dir(sys.argv[1].replace("\\", "/"))  # sys.argv[1] is a passed file path.
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
