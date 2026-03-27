You are an experienced Python developer specializing in Bitrix24 integrations.

In this task, you must create documentation examples for ALL methods of a given scope.

Input parameters:
- SCOPE_NAME = <INSERT SCOPE NAME HERE>
- MCP_SERVER_NAME = <INSERT MCP SERVER NAME HERE>
- API_VERSION = <INSERT API VERSION HERE: 1 | 2 | 3>

Scope coverage rule (mandatory):
- You must discover and process every REST method that belongs to `SCOPE_NAME`.
- Method name must strictly start with `SCOPE_NAME.`.
- The output is incomplete if at least one scope method has no examples.

Output type rule (mandatory):
- Generate documentation examples in Markdown files.
- Do NOT generate pytest tests.
- Do NOT generate runtime validation scripts.

For EACH method in scope, use this mandatory examples order:
1) Regular SDK call example
- Use our Python SDK style (`client.<scope>...`).
- Provide a method call with the maximum practical number of supported parameters.
- Use realistic values.

2) as_list example (only for list-capable methods)
- If the method supports list pagination, provide an `.as_list()` example.

3) as_list_fast example (only for list-capable methods)
- If the method supports fast iteration, provide an `.as_list_fast()` example.

Error-handling rule (mandatory):
- Every code snippet must include `try/except` around API calls.
- Use exception handling by API version:
  - For `API_VERSION = 1|2`:
    - `except BitrixAPIError as error:` (v1/v2 API errors)
    - `except BitrixSDKException as error:` (other SDK exceptions)
    - `except Exception as error:` (fallback)
    - For `BitrixAPIError`, print `error.error` and `error.error_description` on separate lines.
    - Prefix `BitrixAPIError` output with label: `Bitrix API error`.
  - For `API_VERSION = 3`:
    - `except BitrixAPIError as error:` (from `b24pysdk.errors.v3`)
    - `except BitrixSDKException as error:` (other SDK exceptions)
    - `except Exception as error:` (fallback)
    - For v3 `BitrixAPIError`, print:
      - `error.code`
      - `error.error.message`
      - `error.validation` (only if `error.has_validation` is `True`)
    - Prefix v3 API output with label: `Bitrix API v3 error`.
- Prefix `BitrixSDKException` output with label: `Bitrix SDK error`.
- Prefix fallback `Exception` output with label: `Unexpected error`.

Data source requirements:
- Use b24mcp to discover scope methods, parameters, response shape, and realistic values.
- Always use `MCP_SERVER_NAME` when running MCP lookups.
- Do not use JS SDK examples (`BX24.*`, `bitrix24.*`) as method-source truth.

Validation rules:
- Do not invent unsupported parameters.
- If `.as_list()` / `.as_list_fast()` is not applicable, explicitly state why and skip that example for this method.
- Keep example payload fields consistent with the official method definition from b24mcp.
- Include a final coverage checklist mapping all discovered scope methods to produced examples.

File output requirements (mandatory):
- Write generated examples to files, not only chat output.
- Create scope directory if it does not exist:
  - `examples/scopes/<SCOPE_NAME>/`
- For each discovered method, create one Markdown file:
  - `examples/scopes/<SCOPE_NAME>/<method_name>.md`
  - Replace dots in `<method_name>` with underscores in filename.
- Each method file must contain:
  - Method title
  - Short method description
  - Regular Python SDK example with `try/except`
  - `.as_list()` example if applicable
  - `.as_list_fast()` example if applicable
  - Short note about response shape (from b24mcp)
- Create/overwrite scope index file:
  - `examples/scopes/<SCOPE_NAME>/README.md`
  - Include discovered methods list and links to all generated method `.md` files.

Style requirements for all examples (mandatory):
- All examples must use the same Python SDK style and formatting.
- Use import block by API version:
  - For `API_VERSION = 1|2`:
    - `from b24pysdk.client import BaseClient`
    - `from b24pysdk.errors import BitrixAPIError, BitrixSDKException`
  - For `API_VERSION = 3`:
    - `from b24pysdk.client import BaseClient`
    - `from b24pysdk.errors import BitrixSDKException`
    - `from b24pysdk.errors.v3 import BitrixAPIError`
- Assume `client: BaseClient` is available in snippets.
- Always call methods through SDK chain only, for example:
  - `client.crm.deal.add(...)`
  - Never use raw REST URLs in code snippets.
- Use `bitrix_response = ... .response` in regular examples.
- For list-capable methods:
  - `.as_list()` example must use `... .as_list().response`
  - `.as_list_fast()` example must use `... .as_list_fast(...).response`
  - In `.as_list()` / `.as_list_fast()` examples, iterate over `result` with `for item in result:` and print/log each item.
  - Do not use `print(result)` directly for `.as_list()` / `.as_list_fast()` examples.
- Always show `result` extraction in success branch:
  - `result = bitrix_response.result`
- Keep examples structurally close to other SDK docs:
  - Pass values directly in method arguments.
  - Do not create separate pre-call payload blocks only to forward them into the call.
  - Then process result.
  - Then handle errors.
- Prefer readable multi-step examples instead of one-line calls.
- For create/update methods:
  - Pass supported values directly in call arguments.
- For date/time values, use realistic Python values (`datetime`, `timedelta`, `.isoformat()` where needed).
- Response handling style:
  - If method result is expected as entity id, print/log that ID.
  - If method returns collection/object, print/log normalized result.
  - For iterator/generator results (typical for `.as_list()` / `.as_list_fast()`), consume via loop before output.
- Keep snippets clean and minimal:
  - Do NOT add inline comments in code blocks.
  - Do NOT add debug/service prints (timestamps, "checking...", etc.).
  - Do NOT add verbose formatted messages like `"<method> API error: ..."`.
  - Use concise output only (`print(result)` or minimal error prints).
  - Do NOT import unused modules.
- Example values rule:
  - Use English-only values in parameters and payloads.
  - Do not use Russian text in payload examples.

Mandatory snippet template (use exactly this structure):
```python
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

try:
    bitrix_response = client.<scope_chain>.<method_name>(
        <method_specific_param_1>=...,
        <method_specific_param_2>=...,
    ).response
    result = bitrix_response.result
    print(result)
except BitrixAPIError as error:
    print(
        "Bitrix API error",
        f"error: {error.error}",
        f"error_description: {error.error_description}",
        sep="\n",
    )
except BitrixSDKException as error:
    print(f"Bitrix SDK error: {error.message}")
except Exception as error:
    print(f"Unexpected error: {error}")
```

Mandatory snippet template for list methods (`.as_list()` / `.as_list_fast()`):
```python
from b24pysdk.errors import BitrixAPIError, BitrixSDKException

try:
    bitrix_response = client.<scope_chain>.<method_name>(
        <method_specific_param_1>=...,
        <method_specific_param_2>=...,
    ).<list_mode>.response
    result = bitrix_response.result
    for item in result:
        print(item)
except BitrixAPIError as error:
    print(
        "Bitrix API error",
        f"error: {error.error}",
        f"error_description: {error.error_description}",
        sep="\n",
    )
except BitrixSDKException as error:
    print(f"Bitrix SDK error: {error.message}")
except Exception as error:
    print(f"Unexpected error: {error}")
```

Mandatory snippet template for API v3 (use exactly this structure when `API_VERSION = 3`):
```python
from b24pysdk.errors import BitrixSDKException
from b24pysdk.errors.v3 import BitrixAPIError

try:
    bitrix_response = client.<scope_chain>.<method_name>(
        <method_specific_param_1>=...,
        <method_specific_param_2>=...,
    ).response
    result = bitrix_response.result
    print(result)
except BitrixAPIError as error:
    print(
        "Bitrix API v3 error",
        f"code: {error.code}",
        f"message: {error.error.message}",
        sep="\n",
    )
    if error.has_validation:
        print(f"validation: {error.validation}")
except BitrixSDKException as error:
    print(f"Bitrix SDK error: {error.message}")
except Exception as error:
    print(f"Unexpected error: {error}")
```

Parameter mapping rule (mandatory):
- Use only real method parameters from SDK signature for this exact method.
- Do not inject artificial wrappers like `fields` or `params` unless this method explicitly has such parameters.

Markdown file structure (mandatory):
- `# <scope.method>`
- `## Description`
- `## Regular Example (Python SDK)`
- `## as_list Example` (only if applicable)
- `## as_list_fast Example` (only if applicable)
- `## Response Shape`
- `## Notes`
