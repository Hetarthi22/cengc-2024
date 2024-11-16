from api import BundledSubmission, get_session_key
from bundle import Bundle
import time
import sys


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: py main.py ../path/to/testcase/dir")

    with open("../.api_key", "r") as file:
        key = file.read()[:-1]

    session = get_session_key(key)

    bundle = Bundle.from_dir(sys.argv[1])
    submission = BundledSubmission.from_bundle(bundle=bundle, session_key=session)
    submission.submit()

    while not submission.finished():
        print("Waiting for submission to solve...")
        time.sleep(3)


if __name__ == "__main__":
    main()
