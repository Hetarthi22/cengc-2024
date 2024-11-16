from bundle import Bundle


def main() -> None:

    bundle = Bundle.from_dir("../images/tests/2024-02-04 040400")
    print(bundle)


if __name__ == "__main__":
    main()
