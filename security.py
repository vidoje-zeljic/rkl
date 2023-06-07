from werkzeug.security import generate_password_hash

users = {
    "foo": {
        "password": generate_password_hash("pass"),
        "roles": ["admin"]
    },
    "bar": {
        "password": generate_password_hash("pass"),
        "roles": ["read"]
    },
}