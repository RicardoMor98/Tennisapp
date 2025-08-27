from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def root_route(request):
    return Response({
        "message": "Welcome to the Tennis Academy API",
        "endpoints": {
            "profiles": "/api/profiles/",
            "training": "/api/training/",
            "tournaments": "/api/tournaments/",
            "authentication": "/api/auth/",
        }
    })