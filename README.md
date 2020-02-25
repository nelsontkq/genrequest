# jsongenerator

For creating dynamic json bodies for testing, example json bodies for APIs etc.

# Instructions

Create a template file like so:

```yaml
variables:
  name: "{{name()}}"
  endpoint: "{{url()}}"
  user: "{{getenv('USER_NAME')}}"
template:
  url: "{{endpoint}}/v1.0/items"
  userName: "{{user}}"
  userId: "{{user}}_{{random_string(7)}}"
  name: "{{name}}"
  description: "{{sentence()}}"
  address: "{{address()}}"
  dimensions:
    length: 5
    width: 3
    height: 2
    weight: 15
```

or use json

```json
{
  "variables": {
    "name": "{{name()}}",
    "endpoint": "{{url()}}",
    "user": "{{getenv('USER_NAME')}}"
  },
  "template": {
    "url": "{{endpoint}}/v1.0/items",
    "userName": "{{user}}",
    "userId": "{{user}}_{{random_string(7)}}",
    "name": "{{name}}",
    "description": "{{sentence()}}",
    "address": "{{address()}}",
    "dimensions": {
      "length": 5,
      "width": 3,
      "height": 2,
      "weight": 15
    }
  }
}
```

This will output json like so:

```json
{
  "url": "https://www.black-soto.net//v1.0/items",
  "userName": "USER12331",
  "userId": "USER12331_GB59UQ7",
  "name": "Rachel Wright",
  "description": "Parent street they onto behavior surface.",
  "address": "184 Davis Square Dominguezside, IL 37051",
  "dimensions": { "length": 5, "width": 3, "height": 2, "weight": 15 }
}
```
