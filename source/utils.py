create_company_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    },
    "required": [
        "title",
        "description"
    ]
}

update_company_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    }
}

create_worker_schema = {
    "type": "object",
    "properties": {
        "full_name": {
            "type": "string"
        },
        "position": {
            "type": "string"
        },
        "phone_number": {
            "type": "string"
        },
        "company_id": {
            "type": "integer"
        }
    },
    "required": [
        "full_name",
        "position",
        "company_id"
    ]
}

update_worker_schema = {
    "type": "object",
    "properties": {
        "full_name": {
            "type": "string"
        },
        "position": {
            "type": "string"
        },
        "phone_number": {
            "type": "string"
        },
        "company_id": {
            "type": "integer"
        }
    }
}

goods_schema = {
    "type": "array",
    "items": {"type": "object",
              "properties": {
                  "title": {
                      "type": "string"
                  },
                  "description": {
                      "type": "string"
                  },
                  "price": {
                      "type": "number"
                  },
                  "count": {
                      "type": "integer"
                  },
                  "worker_id": {
                      "type": "integer"
                  },
                  "company_id": {
                      "type": "integer"
                  },
                  "tags": {
                      "type": "array"
                  }
              }},
    "required": [
        "title",
        "price",
        "company_id"
    ]

}

assign_worker_to_goods_schema = {
    "type": "object",
    "properties": {
        "worker_id": {
            "type": "integer"
        }
    },
    "required": [
        "worker_id"
    ]
}

update_goods_schema = {
    "type": "object",
    "properties": {
        "description": {
            "type": "string"
        },
        "price": {
            "type": "integer"
        },
        "count": {
            "type": "integer"
        },
        "worker_id": {
            "type": "integer"
        }
    }
}

class NotFound(Exception):
    pass