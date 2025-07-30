import base64
import json
from collections.abc import Callable

from rest_framework import status
from rest_framework.views import APIView

from ardhi_framework.response import ArdhiResponse
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.conf import settings
from django.views.generic import View
import jwt
from ardhi_framework.exceptions import get_exception_response
from ardhi_framework.models import ArdhiBaseModel, ArdhiModel


class ArdhiGeneralView(View):
    pass


class ArdhiBaseView(ArdhiGeneralView):
    # requires that each function to have serializer_class and return success message
    serializer_class = None

    def get_serializer_context(self):
        context = {
            'headers': self.return_headers,
            'user': self.logged_in_user,
            'request_id': self.request_id,
            'request': None,
            'method': self.request.method,
            'active_role': self.active_role,
        }
        return context

    @property
    def active_role(self):
        if self.headers.get('CPARAMS', None) is not None:
            return json.loads((base64.b64decode(self.headers.get('CPARAMS').encode()).decode('utf-8')))['active_role']
        return 'UNKNOWN_ROLE'

    @property
    def request_id(self, req_id=None):
        if not req_id:
            return self.request.query_params.get('request_id', self.request.data.get('request_id', None))
        return req_id

    def decode_jwt(self):
        return jwt.decode(self.headers.get('JWTAUTH').split(' ')[1], settings.SECRET_KEY, algorithms='RS256',
                          options={"verify_signature": True}) or {}

    @property
    def logged_in_user(self):
        return self.decode_jwt().get('user')

    @property
    def return_headers(self):
        headers = {
            'Authorization': self.request.headers.get('Authorization'),
            'JWTAUTH': self.request.headers.get('JWTAUTH'),
            'CPARAMS': self.request.headers.get('CPARAMS')
        }
        return headers

    @staticmethod
    def return_invalid_serializer(serializer):
        return get_exception_response(serializer.errors)

    @staticmethod
    def return_failed(created_response):
        return ArdhiResponse({'details': created_response}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def return_success(data):
        return ArdhiResponse(data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        raise NotImplementedError('View must define a serializer_class attribute.')

    def run_serializer_validator(self, success_msg=None):
        """Processes the serializer through validation to save"""
        context = self.get_serializer_context()
        if context['method'] == 'PATCH':
            self.serializer_class = self.delete_serializer
        serializer = self.get_serializer_class()(
            data=self.request.data,
            context=context
        )
        if not serializer.is_valid():
            return self.return_invalid_serializer(serializer)

        created, created_response = serializer.save()
        if not created:
            return self.return_failed(created_response)
        if created_response is not None:
            if isinstance(created_response, dict):
                created_response['details'] = success_msg
                return self.return_success(created_response)
            elif isinstance(created_response, str):
                return self.return_success({"details": created_response})
        return self.return_success({"details": success_msg})


class ArdhiGenericViewSet(ArdhiBaseView, GenericViewSet):
    """Generic viewset uses action decorators. Modified here"""
    pass


class ArdhiAPIView(ArdhiBaseView, APIView):

    def delete(self, request, *args, **kwargs):
        """No delete method allowed. Override destroy method to perform delete action."""
        return self.return_success('Deleted successfully.')  # we now it has skipped deletion


class ArdhiModelViewSet(ArdhiBaseView, ModelViewSet):
    model: ArdhiBaseModel = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        assert isinstance(self.model, (ArdhiBaseModel, ArdhiModel)), "This view must be used with an Ardhi Custom Model."

    def perform_destroy(self, request, *args, **kwargs):
        # ensure no delete occurs by overriding destroy method
        return


