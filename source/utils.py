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