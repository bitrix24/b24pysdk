### Running Tests

### Preparation
1. Install dev dependencies:
```bash
pip install -r requirements-dev.txt
```
2. Create a .env.local file with the following data(example values):
```txt
B24_DOMAIN=b24-e4f2d1.bitrix24.com
B24_WEBHOOK=13/dd5w3aldjdu4twfk
B24_CLIENT_ID=local.672f30763b63d4.04393872
B24_CLIENT_SECRET=rdsfdcc6RtwHlkFng5145gGdhebdh8mXl12QjaD112frtBSL16
B24_PREFER_AUTH_TYPE=webhook

# Only if you're running the integration tests directly, without first running tests/application_bridge/index.py
B24_ACCESS_TOKEN=b0872d69007e1212107f3e254fb7f1gdsgdv11297667cf03e675caa
B24_REFRESH_TOKEN=a00655dgghd5tfd25df256fd52e5f1f5d60d44b7bd193be0a98869
B24_EXPIRES=2025-11-28 21:09:16+03:00
B24_EXPIRES_IN=3600
B24_EXPIRED_TOKEN=expired_token_value
```
3. (Optional) Create or update `tests/constants_local.py` to override local test constants:
```python
# Local overrides for user constants. 
PROFILE_ONLY_WEBHOOK_TOKEN = "your_webhook_token"
EVENT_HANDLER_URL = "http://localhost:8000"
```

**Important Notes:**

- When installing the application on the portal, it is recommended to specify all scopes for the correct operation of tests

- Tests are designed assuming that the webhook/application token will have administrator privileges

4. Run tests/application_bridge/index.py:
    - In your IDE: Right-click on the file and select "Run"
    - Via command line:
    ```bash
    fastapi dev tests/application_bridge/index.py
    ```
5. Navigate to the application whose data you specified in step 2, and set the `Handler URL` to `http://localhost:8000`.
6. Launch the application. A file named `oauth_data.json` should appear in your `tests/` directory, containing:
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
- Run all tests with code coverage check:
  ```bash
  pytest --cov=b24pysdk tests/
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

- Run all tests in the project with code coverage check:
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

- Execute all unit tests located in the `tests/unit` directory:
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
