# C-Eng-C 2024

## Challenge

Determine the geographic coordinates of a high-sailing pirate ship using pictures of the starts at bow, stern, port, and starboard. The ship's heading, the date, and local solar time is London (longitude 0).

## Installation/Usage

- Requires Python 3.12.0+ ([Download Python](https://www.python.org/downloads/))
- Clone the repository:

  ```bash
  git clone https://github.com/Hetarthi22/cengc-2024.git
  ```

- Run the following command in termnal to install all program requirements

  ```bash
  pip install -r requirements.txt
  ```

- Paste the absolute file path to the index.html and about.html files into your browser to view the UI.

To run the backend, use the following command from within the project directory.

```console
python ./src/main.py <path/to/test/case/directory>
```
For example:

```console
python .\src\main.py '.\images\tests\2024-02-04 040400'
```

It is important you do not leave a trailing slash on the path name.

## Citations

Our program makes use of a publicly available API for annotating and analyzing constellation images. This service is
provided by [Astrometry.net][api-site]

### Libraries Used

- [requests](https://docs.python-requests.org/en/latest/index.html)

## Authors

- Matteo Golin
- Hetarthi Soni
- Hamnah Qureshi
- Grant Achuzia

[api-site]: https://nova.astrometry.net/api_help
