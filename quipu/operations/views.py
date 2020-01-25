from django.utils.translation import gettext as _

from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OperationSerializer


class OperationView(APIView):
    """"""
    operation_type = None

    def get(self, *args, **kwargs):
        """"""
        # TODO: abstract versioning to a mixin?
        if self.request.version and self.request.version != '1':
            raise APIException(_("Unsuported version"))

        self.request.data.update({'a_type': self.operation_type})
        serializer = OperationSerializer(data=self.request.data)
        if serializer.is_valid():
            result_data = {
                "inputs": self.request.data,
                "result": serializer.perform_operation()
                }
            return Response(result_data, status=status.HTTP_200_OK)
        else:
            # TODO: use a better status code?
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimpleCalculatorView(APIView):
    """"""
