from rest_framework.request import Request
class TokenAuth:
    def get_token(self, request: Request):
        auth_header = request.headers.get("Authorization", "")
        return auth_header