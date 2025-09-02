# Introduction

---

B24PySDK is the official library for working with the Bitrix24 REST API in Python.

It offers following advantages:
1. Supports authorization via tokens and webhooks;
2. Allows to pass arguments and retreive response data as native Python types;
3. Utilizes type hints to show possible method arguments and their types;
4. Checks that passed arguments have valid types.

# Documentation

---

The REST API documentation can be found on [Bitrix24 REST API](https://apidocs.bitrix24.com/).

# Quickstart

---

This section provides a short guide to help you get started with B24PySDK.

The following examples illustrate common scenarios when using the library.
## Calling an API method

---

To call Bitrix API, import Client and BitrixWebhook or BitrixToken classes from the library and create class objects.
There are two ways of calling API methods via library.
1. Using a permanent incoming local webhook code: https://apidocs.bitrix24.com/local-integrations/local-webhooks.html

```python
from b24pysdk import BitrixWebhook, Client

bitrix_token = BitrixWebhook(domain="your_bitrix_portal", auth_token="key_of_your_webhook")
client = Client(bitrix_token)
```

2. Using a temporary OAuth 2.0 authorization token: https://apidocs.bitrix24.com/api-reference/oauth/index.html

```python
from b24pysdk import BitrixToken, Client, BitrixApp

bitrix_app = BitrixApp(client_id="app_code", client_secret="app_key")
bitrix_token = BitrixToken(
    domain="your_bitrix_portal", 
    auth_token="key_of_your_webhook", 
    refresh_token="refresh_token_of_the_app", # optional parameter
    bitrix_app=bitrix_app,
)
client = Client(bitrix_token)
```

Client class is your access point to the API. All supported methods can be called using properties of created instance.

For example, to get a description of deal fields we can use REST method crm.deal.fields like so:
```python
response = client.crm.deal.fields()
```

## Passing parameters in API calls

---

Most of Bitrix REST API methods allow you to pass some arguments to them. In order to send them using SDK, simply pass these arguments as positional or named arguments to the corresponding Python function.

To illustrate, we can update a deal by calling: 
```python
response = client.crm.deal.get(bitrix_id=2)
```

## Retrieving results of the call

---

B24PySDK uses deferred method calls. To invoke a method and obtain its result, access the corresponding property. 
The JSON response retrieved from the server is automatically parsed and stored in an object: 
response.result contains the value returned by the API method, while response.time provides the execution time of the request.
```python
from b24pysdk import BitrixWebhook, Client

bitrix_token = BitrixWebhook(domain="your_bitrix_portal", auth_token="key_of_your_webhook")
client = Client(bitrix_token)

response = client.crm.deal.update(bitrix_id=10, fields={'TITLE': 'New title'})
print(f'Updated successfully: {response.result}')
print(f'Call took {response.time.duration} seconds')
```
```
Updated successfully: True
Call took 0.40396690368652344 seconds
```
For list methods, you can use .as_list() and .as_list_fast() to explicitly convert the result into a list.  
The .as_list() method returns up to 50 records and supports pagination to retrieve additional results.  
```python
response = client.crm.deal.list()
deals = response.as_list().result
```
The .as_list_fast() method is optimized for handling large datasets and returns all records in a single call.
```python
response = client.crm.deal.list()
deals = response.as_list_fast().result
```