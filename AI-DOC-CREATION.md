#### Code Documentation Rules

This document defines the standard rules for writing documentation (docstrings) in our project. All code descriptions must follow a consistent structure and style as shown in the provided example.

---

#### 1. General Principles

* All public classes, methods, and functions MUST include a docstring.
* Docstrings must be written in clear, professional English.
* Use triple double quotes (`"""`) for all docstrings.
* Follow a consistent structure and formatting across the entire project.
* Keep descriptions concise, accurate, and focused on behavior, not implementation details.

---

#### 2. Class Docstring Structure

Every class docstring must follow this template:

```
"""
Short one-line class description.

Documentation: <URL to official or related documentation>
"""
```

##### Rules:

* The first line is a short summary of the class responsibility.
* Use an imperative or descriptive tone (e.g. "Handle operations related to...").
* Provide a direct link to official documentation when available.
* Leave a blank line between the description and the Documentation link.

---

#### 3. Method / Function Docstring Structure

Each method with @type_checker decorator must follow this exact structure:

```
"""
Short summary of what the method does.

Documentation: <URL>

Optional extended explanation of the method behavior.

Args:
    param1: Description of the parameter.
    
    param2: Description of the parameter.

Returns:
    Description of the return value.
"""
```

##### Required Sections:

1. **Summary**

   * One short sentence describing the purpose of the method.
   * Starts with a verb (e.g. Retrieve, Create, Update, Delete, Fetch).

2. **Documentation Link**

   * Must include a direct reference to official documentation.

3. **Extended Description (Optional)**

   * Explains how the method works or what it affects.
   * Should clarify business logic or API behavior if needed.

4. **Args Section**

   * Lists all parameters in the order they appear in the method signature.
   * Format:

     ```
     Args:
         parameter_name: Description of the parameter;
     ```
   * Each parameter must have a clear explanation.

5. **Returns Section**

   * Clearly describes the return value or object type.
   * Always specify what the caller receives.

---

#### 4. Formatting Rules

* Use 4 spaces for indentation inside docstrings.
* Separate logical sections with a blank line.
* Always end descriptions with proper punctuation.
* Avoid redundant information.
* Do not include implementation details or internal logic.

---

#### 5. Naming and Language Style

* Use formal technical English.
* Avoid slang or informal expressions.
* Prefer action-oriented verbs for method descriptions:

  * Fetch
  * Retrieve
  * Process
  * Generate
  * Validate
  * Send

---

#### 6. Example Template

##### Class Example

```
class Workgroup(BaseEntity):
    """Handle operations related to Bitrix24 workgroups.

    Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/index.html
    """
```

##### Method Example

```
@type_checker
    def get(
            self,
            params: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve information about a specific workgroup.

        Documentation: https://apidocs.bitrix24.com/api-reference/sonet-group/socialnetwork-api-workgroup-get.html

        This method fetches details of the workgroup based on the provided parameters.

        Args:
            params: Parameters to be sent with the API requests;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "params": params,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
```

---

#### 7. Special Rules for Complex Parameters (Object / Structured Params)

For some parameters you should add extra description including type description shown in the example below.

##### Rules
* Use JSON-like structure and `Object format` keyword for JSONDict type describing nested parameters;
* Always end the structure description with a semicolon `;`;
* Use capitalized keys only if required by the external API;
* Always include explanation of both key and value meaning.

##### Example:
```
filter: Object format:
    {
        "field_1": "value_1",

        "field_2": "value_2",

        ...,

        "field_n": "value_n",

    }, where ENTITY_ID and ENTITY_TYPE are required fields;

order: Object format:

    {
        field_1: value_1,

        ...,
    }

        where

        - field_n is the name of the field by which the selection will be sorted

        - value_n is a string value equals to 'ASC' (ascending sort) or 'DESC' (descending sort);
            
fields: Object format:
    {
        "ENTITY_ID": 'value',

        "ENTITY_TYPE": 'value',

        "COMMENT": 'value',

        "AUTHOR_ID": 'value',

        "FILES": [
            [ "file name", "file content" ],

            [ "file name", "file content" ],
        ]
    };
    
item_type: Type of the record to which the note should be applied:

    - 1 — history record;
    
    - 2 — deal;
```

---

#### 8. Enforcement

* All new code must comply with these documentation rules.
* Code reviews must include verification of docstring format.
* Non-compliant documentation must be corrected before merge.

---

Following this standard ensures maintainable, readable, and professional documentation across the project.
