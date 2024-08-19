from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet


class CommonViewSet:
    """
    Common view set for all view sets
    - create response
    - get resource URI
    """

    def ok(self, data: dict | None = None) -> Response:
        """
        Default response ok. Status code is 200
        """
        return Response(data=data, status=status.HTTP_200_OK)

    def created(self, data: dict | None = None) -> Response:
        """
        Default response created. Status code is 201
        """
        return Response(data=data, status=status.HTTP_201_CREATED)

    def no_content(self) -> Response:
        """
        Default response no content. Status code is 204
        """
        return Response(status=status.HTTP_204_NO_CONTENT)

    def not_found(self) -> Response:
        """
        Default response not found. Status code is 404
        """
        return Response(status=status.HTTP_404_NOT_FOUND)

    def forbidden(self, data: dict | None = None) -> Response:
        """
        Default response forbidden. Status code is 403
        """
        if not data:
            data = {
                "detail": "You do not have permission to perform this action.",
            }

        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    def bad_request(self, message=None, code=None):
        """
        Return bad request with message content & code
        """
        # Build up the error content.
        response_data = (
            {
                "message": message,
                "code": code,
            }
            if (message or code)
            else None
        )

        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_resource_uri(self):
        """
        Get resource URI
        """
        domain = settings.DOMAIN
        api_root = "/api/v1/"

        return f"{domain}{api_root}{self.resource_name}/"


class PaginationViewSet:
    """
    View set for pagination
    """


class FilteringViewSet:
    """
    View set for filtering
    """


class AuthenticatedViewSet:
    permission_classes = [IsAuthenticated]


class BaseViewSet(ViewSet, CommonViewSet, AuthenticatedViewSet):
    """
    Base view set for views accept DTO data rather than Django model
    """


class BaseModelViewSet(ModelViewSet, CommonViewSet, AuthenticatedViewSet):
    """
    Base view set for Django model
    """
