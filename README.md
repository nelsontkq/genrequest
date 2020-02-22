# jsongenerator

For creating dynamic json bodies for testing, example json bodies for APIs etc.


# Instructions

Create a template yaml file like so:

```yaml
variables:
  name: "{{name()}}"
  endpoint: "{{url()}}"
  user: "{{getenv('USER_NAME')}}"
template:
  url: "{{endpoint}}/v1.0/items/api"
  customerCode: "{{customer}}"
  sku: "{{sku}}"
  name: "{{name}}"
  description: "{{sentence()}}"
  address: "{{address()}}"
  dimensions:
    length: 5
    width: 3
    height: 2
    weight: 15
```

will output json like so:  

```json

```