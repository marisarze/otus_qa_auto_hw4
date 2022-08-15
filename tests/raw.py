schema = {
            'status': {'type': 'string'},
            'message': {'type': 'list', 'schema': {'type': 'string'}}
        }
        v = cerberus.Validator(schema)
        assert v.validate(r.json())