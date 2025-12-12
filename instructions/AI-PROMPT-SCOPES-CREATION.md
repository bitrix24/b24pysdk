You are an experienced Python developer specializing in Bitrix24 integration and building clean, standardized API client architectures. 

In this task, you will be working with scope: <INSERT HERE YOUR SCOPE NAME FROM DOCUMENTATION>, which will henceforth be referred to as "SCOPE".

Your primary goal is to scan the provided b24mcp documentation and identify all API methods that strictly belong to this SCOPE.

You must find all API methods whose names strictly match the following regular expression: ^{SCOPE}\. This means the method name must begin exactly with "SCOPE." (e.g., if SCOPE is crm.lead, look for crm.lead.add, crm.lead.list).

Important Exclusion Rules: Do not use any information from the JS SDK documentation to identify API methods. Specifically:
    Ignore methods starting with BX24. or bitrix24. (e.g., BX24.callMethod or BX24.SCOPE.call do not qualify).
    Ignore JavaScript function descriptions/signatures.
    You need raw REST API method names only.

Use only information from the provided documentation. If any information is missing from the documentation, do not infer, guess, or supplement it.

Only after you have obtained the complete, verified list of methods that strictly satisfy the criteria, proceed to the next stage described in the text.

Your task is to create a new class based strictly on the following manual, using exclusively information from the provided source. 
You must not deviate in any way from this manual.

The class creation manual is located in the file:

AI-SCOPES-CREATION-README.md

Write me the full version of the class code, implemented strictly according to the instructions in the manual above and incorporating ALL previously selected API methods — each of which must satisfy the selection criteria.
**Ensure that the class includes methods for all identified API endpoints matching the pattern. Do not limit the implementation to a subset; the final class must represent a complete client for the specified scope based on the documentation.** 
**When constructing the class architecture, you must follow exactly what is specified in section 5 of the manual. Adherence to the architectural guidelines in section 2 is mandatory. Adherence to the code style in sections 6 and 7.1 in mandatory**