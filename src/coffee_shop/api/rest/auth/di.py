from coffee_shop.api.rest.auth.service import AuthService


def auth_service_dependency():
    return AuthService()
