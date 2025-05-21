# Introduction
B24PySDK is the official library for working with the Bitrix24 REST API in Python

It offers following advantages:
1. Supports authorization via tokens and webhooks
2. Allows to pass arguments and retreive response data as native Python types
3. Utilizes type hints to show possible method arguments and their types
4. Checks that passed arguments have valid types

# Quickstart
This section gives an introduction in how to get started with B24PySDK
Let's get started with some simple examples
### Calling an API method
To call Bitrix API, begin by importing Client and BitrixToken classes

```python
from b24pysdk import BitrixToken, Client
```
Then create instances of these classes:
```python
bitrix_token = BitrixToken(domain="yourbitrixportal", auth_token="<key of your webhook>", is_webhook=True)
client = Client(bitrix_token)
```
BitrixToken represents one of the two possible options for passing authorization data in requests to the REST API:
- Specifying a permanent incoming local webhook code;
- Specifying a temporary OAuth 2.0 authorization token, which is used in local and mass-market applications.

Client class is your accesss point to the API. All supported methods can be called using properties of created instance.

For example, to get a description of deal fields we can use REST method crm.deal.fields like so:
```python
response = client.crm.deal.fields()
```
### Passing parameters in API calls
Most of Bitrix REST API methods allow you to pass some arguments to them. In order to send them using SDK, simply pass these arguments as positional or named arguments to the corresponding Python function.
For example, we can update a deal by calling 
```python
response = client.crm.deal.get(bitrix_id=2)
```
### Retrieving results of the call
We can retrieve results of our call to Bitrix REST API. For example, crm.deal.update will return true if deal was successfully updated:

```python
from b24pysdk import BitrixToken, Client

bitrix_token = BitrixToken(domain="yourbitrixportal", auth_token="<key of your webhook>", is_webhook=True)
client = Client(bitrix_token)

response = client.crm.deal.update(bitrix_id=10, fields={'TITLE': 'New title'})
```
B24PySDK will parse JSON retrieved from the server and place it in an object.
response.result will contain a value returned by corresponding API method, 
and response.time will contain information about execution time of the request

```python
print(f'Updated successfully: {response.result}')
print(f'Call took {response.time.duration} seconds')
```
```
Updated successfully: True
Call took 0.40396690368652344 seconds
```