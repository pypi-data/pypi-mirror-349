# Connector Definition Runner

This package provides the framework for connectors to be created with only schemas.  It can make HTTP 
calls based on what is defined in the schema.
## Asset Schema Structure

The asset schema defines the authentication that is used for the connector. 

We currently support the following authentication methods:
* API Key (in the header, query parameters, or cookie)
* OAuth2
  * Client Credential
  * Password Grant
* HTTP Basic
* HTTP Bearer Token

Each authentication type has an asset file name and inputs that it requires. There is also a 
`meta.security` key in the asset schema that contains the configuration for the authentication.
The asset file name must match the `name` field, unless it's a custom asset (See the examples below).

Examples:

### http_basic

```yaml
schema: asset/1
name: http_basic
title: HTTP Basic Authentication
description: 'Authenticates using username and password.'
inputs:
  type: object
  properties:
    url:
      title: URL
      description: A URL to the target host.
      type: string
      default: https://www.example.com # change if it has a default cloud URL or remove if always custom.
    username:
      title: Username
      description: Username
      type: string
    password:
      title: Password
      description: Password
      type: string
      format: password
    verify_ssl:
      title: Verify SSL Certificates
      description: Verify SSL certificate
      type: boolean
    http_proxy:
      title: HTTP(s) Proxy
      description: A proxy to route requests through.
      type: string
  required:
    - url
    - username
    - password
meta:
  security:
    type: http
    scheme: basic
```

### http_bearer

```yaml
schema: asset/1
name: http_bearer
title: HTTP Bearer Authentication
description: 'Authenticates using bearer token such as a JWT, etc.'
inputs:
  type: object
  properties:
    url:
      title: URL
      description: A URL to the target host.
      type: string
      default: https://www.example.com # change if it has a default cloud URL or remove if always custom.
    token: # NEVER CHANGE THIS
      title: Token # name this properly
      description: The API key, token, etc. # name this properly
      type: string
      format: password
    verify_ssl:
      title: Verify SSL Certificates
      description: Verify SSL certificate
      type: boolean
    http_proxy:
      title: HTTP(s) Proxy
      description: A proxy to route requests through.
      type: string
  required:
    - url
    - username
    - password
meta:
  security:
    type: http
    scheme: bearer
```
### apikey
```yaml
schema: asset/1
name: apikey
title: API Key Authentication
description: 'Authenticates using an API Key'
inputs:
  type: object
  properties:
    url:
      title: URL
      description: A URL to the target host.
      type: string
      default: https://www.example.com # change if it has a default cloud URL or remove if always custom.
    x-apikey: # example, replace with correct key name for product.
      title: API Key
      description: API key
      type: string
      format: password
    verify_ssl:
      title: Verify SSL Certificates
      description: Verify SSL certificate
      type: boolean
    http_proxy:
      title: HTTP(s) Proxy
      description: A proxy to route requests through.
      type: string
  required:
    - url
    - x-apikey # example, replace with correct key name for product.
meta:
  security:
    type: apiKey
    name: x-apikey # example, replace with correct key name for product.
    in: header, cookie or query # please select the one applicable to the API and remove the others.

```

The `security` field inside `meta` could be an object or an array of objects. 

**Examples:**

If you need to make a request with the header field `x-apikey` and add its value from the inputs, you can use the following schema. 
In this case the `x-apikey` input field is mandatory.

```yaml
inputs:
  type: object
  properties:
    x-apikey: # example, replace with correct key name for product.
      title: API Key
      type: string
      format: password
meta:
  security:
    name: x-apikey
    in: header
```

You can also define a template using mustache syntax with the input values. For example, if you want 
to add to your header the field `Authorization: ApiToken my_token`, you can use the following schema
and use `my_token` as an input value. 


```yaml
inputs:
  type: object
  properties:
    token: # example, replace with correct key name for product.
      title: Token
      type: string
      format: password
meta:
  security:
    name: Authorization
    in: header
    format: ApiToken {{token}}
```

### oauth2_client_credentials

The optional field `meta.security.token_endpoint` on this example can be used to set a token endpoint which will be 
concatenated to the `url` input to create the token url.  If you provide a `token_endpoint`, the `token_url` input
should not be required.

```yaml
schema: asset/1
name: oauth2_client_credentials
title: Oauth 2.0 Client Credentials
description: 'Authenticates using oauth 2.0 client credentials'
inputs:
  type: object
  properties:
    url:
      title: URL
      description: A URL to the target host.
      type: string
      default: https://www.example.com # change if it has a default cloud URL or remove if always custom.
    token_url:
      title: Token URL
      type: string
      default: https://www.example.com/oauth/token # remove if this is static. Graph API requires tenant ID and would need the user input.
    client_id:
      title: Client ID
      description: The client ID
      type: string
    client_secret:
      title: Client Secret
      description: The client secret.
      type: string
      format: password
    scope:
      title: Scope
      description: Permission scopes for this action.
      type: array
      items:
        type: string
      default: [] # Add array of scopes we think are needed for the action.
    verify_ssl:
      title: Verify SSL Certificates
      description: Verify SSL certificate
      type: boolean
    http_proxy:
      title: HTTP(s) Proxy
      description: A proxy to route requests through.
      type: string
  required:
    - url
    - client_id
    - client_secret
    - token_url
meta:
  security:
    token_endpoint: "api/oauth2/token"
    type: oauth2
    flow: client_credentials
```

### oauth2_password

The optional field `meta.security.token_endpoint` on this example can be used to set a token endpoint which will be 
concatenated to the `url` input to create the token url.  If you provide a `token_endpoint`, the `token_url` input
should not be required.

```yaml
schema: asset/1
name: oauth2_password
title: Oauth 2.0 Password Grant
description: 'Authenticates using oauth 2.0 client credentials'
inputs:
  type: object
  properties:
    url:
      title: URL
      description: A URL to the target host.
      type: string
      default: https://www.example.com # change if it has a default cloud URL or remove if always custom.
    token_url:
      title: Token URL
      type: string
      default: https://www.example.com/oauth/token # remove if this is static. Graph API requires tenant ID and would need the user input.
    oauth2_username:
      title: OAuth2 Username
      description: The username for authentication
      type: string
    oauth2_password:
      title: OAuth2 Password
      description: The password for authentication
      type: string
      format: password
    client_id:
      title: Client ID
      description: The client ID
      type: string
    client_secret:
      title: Client Secret
      description: The client secret.
      type: string
      format: password
    scope:
      title: Scope
      description: Permission scopes for this action.
      type: array
      items:
        type: string
      default: [] # Add array of scopes we think are needed for the action.
    verify_ssl:
      title: Verify SSL Certificates
      description: Verify SSL certificate
      type: boolean
    http_proxy:
      title: HTTP(s) Proxy
      description: A proxy to route requests through.
      type: string
  required:
    - url
    - oauth2_username
    - oauth2_password
    - token_url
meta:
  security:
    token_endpoint: "api/oauth2/token"
    type: oauth2
    flow: password
```

## Action Schema Structure

The action schema will include the following fields:

* schema: The schema type, this differentiates the assets from actions.
* title: The action title
* name: The action internal name
* description: The action description
* inputs: object of input fields
* output: object with the output fields
* meta:
  * endpoint: The HTTP endpoint
  * method: The HTTP method

Example schema:

```yaml
schema: action/1
title: Delete Indicator
name: delete_indicator
description: Deletes an indicator
inputs:
  type: object
  properties:
    json_body:
      title: JSON Body
      type: object
      properties:
        id:
          title: ID
          type: string
      required:
        - id
      additionalProperties: false
  required: 
    - json_body
  additionalProperties: falase
output:
  type: object
  properties:
    status_code:
      title: Status Code
      type: number
meta:
  endpoint: iocs/entities/indicators/v1
  method: DELETE
```
### Inputs

The `inputs` field must be an object type with the following properties:

* headers: Headers to send with the request.
* parameters: Parameters to send in the query string for the request.
* data_body: Raw data send in the body of the request.
* json_body: JSON data to send in the body of the request.
* files: Object or array of objects with the `contentDisposition: attachment` property. 
* path_parameters: Parameters to be replaced in the URL.


**Path Parameters**

You can use mustaches to build the URL path based in the `path_parameters` values. For example, if you have the following URL:

```
https://api.crowdstrikefalcon/{{session_id}}/download/{{filename}}
```

and the following `path_parameters` inputs field:


```yaml
inputs:
  type: object
  properties:
    path_parameters:
      title: Path Parameters
      type: object
      properties:
        session_id:
          title: Session ID
          type: string
        filename:
          title: File Name
          type: string
      required:
        - session_id
        - filename
```

Then the endpoint will be formatted using the input data in the `path_parameters` object.


**Files**

`files` inputs could also include binary inputs and additional properties for the file. For example:

```yaml
inputs:
  type: object
  properties:
    attachments:
      title: Attachments
      type: array
      items:
        contentDisposition: attachment
        type: object
        additionalProperties: false
        properties:
          file:
            type: string
            format: binary
          file_name:
            type: string
      examples: []
  required:
    - attachments
  additionalProperties: true
```

You can also add additional properties into the attachment properties. For example, if you need to replicate the following
code:

```python
import requests

headers = {
    'accept': 'application/json'
}

files = [
    ('file', open('decode.py;type=text/x-python-script', 'rb')),
    ('permission_type', (None, 'public')),
    ('platform', (None, 'linux'))
]

response = requests.post('https://api.crowdstrike.com/real-time-response/entities/scripts/v1', headers=headers, files=files)
```

You can use the following input:

```yaml
inputs:
  type: object
  properties:
    attachments:
      title: Attachments
      type: array
      items:
        contentDisposition: attachment
        type: object
        additionalProperties: false
        properties:
          file:
            type: string
            format: binary
          file_name:
            type: string
          permission_type:
            type: string
          platform:
            type: string
  required:
    - attachments
  additionalProperties: true
```


### Outputs

The `output` field works similar to `inputs`, with the difference that it could be an array instead of an object.

It will contain the following properties:

* `status_code`: The status code of the response.
* `response_headers`: The headers of the response.
* `reason`: A text corresponding to the status code. For example, OK for 200, Not Found for 404.
* `json_body`: A JSON object of the response
* `response_text`: If the response doesn't contain a JSON body and there is no `file` property defined in the manifest, the response body will be returned in text format. 
* `file`: Object or array of objects with the `contentDisposition: attachment` property.

In order to get files as output, you must manually add a file property to the output section. See the following example:

```yaml
output:
  type: object
  properties:
    attachments:
      title: Attachments
      type: array
      items:
        contentDisposition: attachment
        type: object
        additionalProperties: false
        properties:
          file:
            type: string
            format: binary
          filename:
            type: string
  additionalProperties: true
```

## Custom Action

In order to add custom actions, you must create a `.py` file and its file name must match with the corresponding manifest.
The source code must have a `RunnerOverride` class with the following interface:

```python
class RunnerOverride:

  def __init__(self, asset=asset, asset_schema=asset_schema, http_proxy=http_proxy):
    pass

  def run(self, inputs=inputs, action_schema=action_schema):
    pass
```

For example, suppose you want to create an action that makes an add operation using LDAP protocol. 
You can create the following schema in `connector/config/actions/add.yaml`:

```yaml
schema: action/1
title: Add
name: add
description: >-
  The Add operation allows a client to request the addition of an entry into the
  LDAP directory.
inputs:
  type: object
  properties:
    dn:
      title: Dn
      examples:
        - CN=Charles,OU=friends,DC=testdomain,DC=local
      type: string
    object_class:
      title: Object Class
      examples:
        - - person
      type: array
      items:
        type: string
    attributes:
      title: Attributes
      examples:
        - name: Charles Darwin
      type: object
      properties:
        name:
          title: Name
          examples:
            - Charles Darwin
          type: string
      required: []
      additionalProperties: true
  required:
    - dn
    - object_class
  additionalProperties: true
output:
  type: object
  properties:
    result:
      title: Result
      type: number
    description:
      title: Description
      type: string
    dn:
      title: Dn
      type: string
    message:
      title: Message
      type: string
    referrals:
      title: Referrals
      type: object
      properties: {}
      required: []
      additionalProperties: true
    type:
      title: Type
      type: string
  required: []
  additionalProperties: true
meta: {}
```

And then create the file `connector/src/add.py` with the source code:

```python

import json
import os
from ldap3 import Server, Connection


class RunnerOverride(LdapActionBasic):

    def __init__(self, asset=asset, asset_schema=asset_schema, http_proxy=None):
        self.server = Server(asset["ip"],
                            use_ssl=asset.get("verify_ssl", True),
                            connect_timeout=asset.get("connect_timeout", 10))
        self.conn = Connection(self.server,
                              asset["username"],
                              asset["password"],
                              auto_bind=True)

    def run(self, inputs=inputs, action_schema=None):
        self.conn.add(inputs)
        return self.conn.result
```

## Custom Authentication

In order to add custom authentication, you must create a `runner_override.py` file.
The file must have a `RunnerOverride` class with the following interface:

```python
class RunnerOverride:

  def __init__(self, asset=asset, asset_schema=asset_schema, http_proxy=http_proxy):
    pass

  def run(self, inputs=inputs, action_schema=action_schema):
    pass
```
When this file is present, all actions will use it.


## Custom headers

You can build your own header field templates using mustache syntax. For example
if you need to define a custom header field like: `auth: my_username:my_password` for all your actions, you can define the following asset schema:

```yaml
schema: asset/1
title: HTTP Custom Authentication
description: 'Authenticates using username and password.'
inputs:
  type: object
  properties:
    url:
      title: URL
      description: A URL to the target host.
      type: string
      default: https://www.example.com # change if it has a default cloud URL or remove if always custom.
    username:
      title: Username
      description: Username
      type: string
    password:
      title: Password
      description: Password
      type: string
      format: password
  required:
    - url
    - username
    - password
meta:
  headers:
    auth: {{username}}:{{password}}
```

This way the username and password will be replaced in the `meta.headers.auth` field. You can also define the same way custom headers for action schemas.
