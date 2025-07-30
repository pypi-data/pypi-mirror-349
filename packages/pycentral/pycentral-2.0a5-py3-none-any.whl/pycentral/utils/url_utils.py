# (C) Copyright 2025 Hewlett Packard Enterprise Development LP.
# MIT License


def urlJoin(*args):
    trailing_slash = "/" if args[-1].endswith("/") else ""
    return "/" + "/".join(map(lambda x: str(x).strip("/"), args)) + trailing_slash


class NewCentralURLs:
    Authentication = {"OAUTH": "https://sso.common.cloud.hpe.com/as/token.oauth2"}

    GLP = {"BaseURL": "https://global.api.greenlake.hpe.com"}

    GLP_DEVICES = {
        "DEFAULT": "/devices/v1/devices",
        # full url requires {id} to be passed as param: /devices/v1/async-operations/{id}
        "GET_ASYNC": "/devices/v1/async-operations/",
    }

    GLP_SUBSCRIPTION = {
        "DEFAULT": "/subscriptions/v1/subscriptions",
        # full url requires {id} to be passed as param: /devices/v1/async-operations/{id}
        "GET_ASYNC": "/subscriptions/v1/async-operations/",
    }

    GLP_USER_MANAGEMENT = {
        "GET": "/identity/v1/users",
        # full url requires {id} to be passed as param: /identity/v1/users/{id}
        "GET_USER": "/identity/v1/users/",
        "POST": "/identity/v1/users",
        # full url requires {id} to be passed as param: /identity/v1/users/{id}
        "PUT": "/identity/v1/users/",
        # full url requires {id} to be passed as param: /identity/v1/users/{id}
        "DELETE": "/identity/v1/users/",
    }

    GLP_SERVICES = {
        "SERVICE_MANAGER": "/service-catalog/v1/service-managers",
        "SERVICE_MANAGER_PROVISIONS": "/service-catalog/v1/service-manager-provisions",
        "SERVICE_MANAGER_BY_REGION": "/service-catalog/v1/per-region-service-managers",
    }
