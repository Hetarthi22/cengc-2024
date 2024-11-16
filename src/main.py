from bundle import Parameters


def main() -> None:

    params = Parameters.from_file(
        "../competition-prompts/images/example cases/example cases/2024-01-01 000000/parameters.json"
    )
    print(params)


if __name__ == "__main__":
    main()
