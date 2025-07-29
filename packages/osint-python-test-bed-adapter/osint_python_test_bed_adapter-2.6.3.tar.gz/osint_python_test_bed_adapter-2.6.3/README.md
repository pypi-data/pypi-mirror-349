# NAAS-PYTHON-KAFKA

This is the Kafka adapter for Python: it allows you to easily connect Python
services to Apache Kafka via Python.

The implementation is a wrapper around [Confluent-Kafka-Python](https://github.com/confluentinc/confluent-kafka-python):

- AVRO schema's and messages: both key's and values should have a schema.
as explained [here](https://github.com/DRIVER-EU/avro-schemas).
- Kafka consumer and producer for the test-bed topics.
- Management
  - Heartbeat (topic: system-heartbeat), so you know which clients are online.
  Each time the test-bed-adapter is executed, it starts a heartbeat process to notify
  the its activity to other clients.

## Installation

You need to install [Python 3+](https://www.python.org/).

To run the examples you will need to install the dependencies specified on the file [requirements.txt](https://github.com/DRIVER-EU/python-test-bed-adapter/blob/master/requirements.txt).

For that, run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt # Or instead of `pip`, use `pip3`
```

from the project folder.

## Examples and usage

- `url_producer`: Creates a message with 4 URLs to RSS feeds on the topic ('system_rss_urls')
- `rss_producer`: Listens to url messages ('system_rss_urls') and produces RSS messages ('system_rss_urls')
- `rss_consumer`: Listens to RSS messages ('system_rss_urls') and prints them to console.

## Uploading to PyPi

1. Ensure you have the necessary tools installed: Make sure you have `setuptools` and `wheel` installed. You can install them using `pip`:

    ```bash
    # Build the distribution files: In the root directory of your project, run the following command to build the distribution files (wheel and source distribution):
    pip install setuptools wheel
    ```

2. Build the distribution files: In the root directory of your project, run the following command to build the distribution files (wheel and source distribution):

    ```bash
    # This command will generate the distribution files inside the dist directory.
    python setup.py sdist bdist_wheel
    ```

    This command will generate the distribution files inside the dist directory.

3. Register an account on PyPI: If you haven't done so already, create an account on PyPI and verify your email address.

4. Install and configure `twine`: Install `twine`, a tool used to upload packages to PyPI, using `pip`:

    ```bash
    # Upload the package to PyPI: Use twine to upload the distribution files to PyPI:
    pip install twine
    ```

5. Upload the package to PyPI: Use twine to upload the distribution files to PyPI:

    ```bash
    # This command will prompt you to enter your PyPI username and password. Once provided, twine will upload the distribution files to PyPI.
    # Use $HOME/.pypirc if you want to use a different configuration file.
    twine upload --repository osint-python-test-bed-adapter dist/*
    ```

    This command will prompt you to enter your PyPI username and password. Once provided, twine will upload the distribution files to PyPI.

6. Verify the package on PyPI: Visit your package page on [PyPI](https://pypi.org/project/osint-python-test-bed-adapter/) to ensure that the package has been successfully uploaded and published.

    Remember to update the version number in your `setup.py` file for each new release to avoid conflicts.

In short:

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Create a new release after updating the setup.py package version number
rm -rf dist
python setup.py sdist bdist_wheel
twine upload --repository osint-python-test-bed-adapter dist/*
```
