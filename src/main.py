from bundle import Parameters


def main() -> None:

    params = Parameters.from_file(
        "../images/tests/2024-02-04 040400/parameters.json"
    )
    print(params)


if __name__ == "__main__":
    main()
