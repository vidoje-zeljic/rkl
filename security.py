from werkzeug.security import generate_password_hash

users = {
    "rkl": {
        "password": generate_password_hash("rkl"),
        "roles": ["admin"]
    },
    # "admin": {
    #     "password": generate_password_hash("admin"),
    #     "roles": ["read"]
    # },
}