A repository for data on EU-financed projects in Romania.

## Setup
* Clone the repository, create a virtualenv, install dependencies:

    ```shell
    pip install -r requirements.txt
    ```

* Copy the local configuration file and customize it:

    ```shell
    cp eurobani/site/example_settings_local.py eurobani/site/settings_local.py
    ```

* Run the sql migrations:

    ```shell
    ./manage.py migrate
    ```

## Import data
* Contracts:

    ```shell
    ./manage.py ingest contracts path/to/contracts.csv
    ```

* Payments:

    ```shell
    ./manage.py ingest payments path/to/payments.csv
    ```
