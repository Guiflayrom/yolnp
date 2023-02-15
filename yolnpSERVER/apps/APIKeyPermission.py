from rest_framework.permissions import BasePermission

class CustomAPIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        auth = bool(request.user and request.user.is_authenticated)
        return auth if auth else request.headers.get("Key") == "4b!^q!z4OGdA6sp^!q3YK8UdFA893F@KOw9fbWvV96sWxeV5Uf"
    