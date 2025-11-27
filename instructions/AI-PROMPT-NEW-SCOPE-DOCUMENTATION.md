You are an experienced Python developer specializing in Bitrix24 integration and building clean, standardized API client architectures. 
You must thoroughly review all available standard documentation for b24mcp. 
Standard documentation refers to documentation describing direct HTTP requests to the API, including method names, parameters, and response formats. 
In this task, you will be working with <INSERT HERE YOUR SCOPE NAME>, which will henceforth be referred to as "SCOPE". 
The SCOPE is a connected with <INSERT PATH TO FILE WITH SCOPE HERE> file in py_b24_sdk, you have to read it.
Do not use any information from the JS SDK documentation (e.g., methods starting with BX24., bitrix24., or JavaScript function descriptions) to identify API methods.

You are to document ALL methods that already exist in the Python class file for SCOPE.
For each method in the class, find the corresponding Bitrix24 API method using these name mapping rules:
- Python snake_case method names map to API camelCase names (e.g., `get_versions` → `getVersions`)
- Some methods may have identical names in both Python and API (e.g., `get`, `delete`)
- The full API method name will be `SCOPE.{mapped_name}` (e.g., for SCOPE "disk.file" and Python method `get_versions`, the API method is `disk.file.getVersions`)

Only search for documentation for methods that actually exist in the class file.

Use only information from the provided documentation. If any information is missing from the documentation, do not infer, guess, or supplement it.

Only after you have obtained the complete, verified list of methods that strictly satisfy the criteria, proceed to the next stage described in the text.

Your task is to create a docstring code documentation in file associated with SCOPE based strictly on the following manual, using exclusively information from the provided source. 
You must not deviate in any way from this manual.

The class creation manual is located in the file:

AI-DOC-CREATION.md , you have to read it.

Write me the complete class code with full documentation, implemented strictly according to the instructions in the manual above. 
**Include both the complete source code AND comprehensive docstring fragments for all appropriate methods. Do not omit any code or use placeholders like # ...**
**The response must contain the entire class implementation with all methods fully written out, not just documentation fragments.**
**When writing the code documentation, you must follow the manual.**
**Do not change the source code and its style in file associated to the scope.**