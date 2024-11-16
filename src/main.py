from api import BundledSubmission, Job, Submission, get_session_key
from bundle import Bundle


def main() -> None:

    with open("../.api_key", "r") as file:
        key = file.read()[:-1]

    session = get_session_key(key)

    bundle = Bundle.from_dir("../images/tests/2024-02-04 040400")
    submission = BundledSubmission.from_bundle(bundle=bundle, session_key=session)
    submission.submit()
    print(submission.get_status())
    print(submission)


if __name__ == "__main__":
    main()
