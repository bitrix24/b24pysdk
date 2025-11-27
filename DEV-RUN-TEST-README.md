### Running Tests

### Preparation
1. Create a .env.local file with the following data(example values):
```txt
B24_DOMAIN=b24-e4f2d1.bitrix24.com
B24_WEBHOOK=13/dd5w3aldjdu4twfk
B24_CLIENT_ID=local.672f30763b63d4.04393872
B24_CLIENT_SECRET=rdsfdcc6RtwHlkFng5145gGdhebdh8mXl12QjaD112frtBSL16
PREFER_AUTH_TYPE=WEBHOOK
```
2. Run tests/application_bridge/index.py:
    - In your IDE: Right-click on the file and select "Run"
    - Via command line (from the tests/application_bridge directory):
    ```bash
    fastapi dev tests/application_bridge/index.py
    ```
3. Navigate to the application whose data you specified in step 1, and set the `Handler URL` to `http://localhost:8000`.
4. Launch the application. A file named `oauth_data.json` should appear in your `tests/` directory, containing:
```txt
{
    "access_token": "",
    "refresh_token": "",
    "expires": "",
    "expires_in": 3600
}
```

#### Local Execution
- Run all tests:
  ```bash
  pytest
  ```
- Run tests without detailed error output:
  ```bash
  pytest --tb=no
  ```
- Run tests for a specific scope by specifying the path to its directory:
  ```bash
  pytest tests/integration/scopes/crm
  ```
- Run tests by marker:
  ```bash
  pytest -m "crm"
  ```

#### Running via Docker
The project defines a make target (`Makefile`) for running scope tests inside a Docker container with parameterization:

- Run all tests in the project:
  ```bash
  make test-all
  ```

- Run tests located in the `tests/integration` directory:
  ```bash
  make test-integration
  ```

- Run integration tests with `AUTH_TYPE` set to `webhook`:
  ```bash
  make test-integration-webhook
  ```

- Run integration tests with `AUTH_TYPE` set to `oauth`:
  ```bash
  make test-integration-oauth
  ```

- Execute all unit tests located in the `tests/integration/unit` directory:
  ```bash
  make test-unit
  ```

- Run tests filtered by a specific pytest marker:
  ```bash
  make test-marker M=your_marker
  ```

- Run tests located at a specific path provided as an argument:
  ```bash
  make test-path TEST_PATH=your/test/path
  ```
