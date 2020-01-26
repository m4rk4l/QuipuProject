from django.utils.translation import gettext as _
from django.core.mail import mail_admins

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from calculator.simple import SimpleCalculator

from .serializers import OperationSerializer, ADDITION, MULTIPLICATION


class CustomOperationSchema(AutoSchema):
    """"""

    def get_operation(self, *args, **kwargs):
        """Custom schema for results.

        TODO:
        * split serializers...
        """
        operations = super().get_operation(*args, **kwargs)

        # FIXME:
        # This is required because we have a single serializer that performs multiple operations
        # From API perspective, this arguments are not required to be passed.
        # Moreover, the dictionaries generated are dependent on the OperationSerializer.
        operations.get('requestBody').get('content').get('application/json').get('schema').get('properties').pop('a_type', None) # noqa
        operations.get('requestBody').get('content').get('application/json').get('schema').get('required').pop(0) # noqa

        operations['responses'] = {
            status.HTTP_200_OK: {
                "input": _("Input given to the request"),
                "result": _("Result calculated by api.")
                },
            status.HTTP_400_BAD_REQUEST: {
                "many": _("details of errors")
            }
        }
        return operations


class AdditionView(GenericAPIView):
    """Perform additions of multiple numbers."""
    serializer_class = OperationSerializer
    schema = CustomOperationSchema()

    def post(self, *args, **kwargs):
        """Perform additions of multiple numbers.

        Arguments:
        `classification` (str): whether the operation is in real or imaginary numbers
        `values`(list): the list of values to be added.
        """
        # TODO: abstract versioning to a mixin?
        if self.request.version and self.request.version != '1':
            raise APIException(_("Unsuported version"))

        self.request.data.update({'a_type': ADDITION})
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=False):
            result_data = {
                "inputs": self.request.data,
                "result": serializer.perform_operation()
                }
            return Response(result_data, status=status.HTTP_200_OK)
        else:
            # TODO: use a better status code?
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MultiplicationView(GenericAPIView):
    """Performs multiplication of multiple numbers."""
    serializer_class = OperationSerializer
    schema = CustomOperationSchema()

    def post(self, *args, **kwargs):
        """"""
        # TODO: abstract versioning to a mixin?
        if self.request.version and self.request.version != '1':
            raise APIException(_("Unsuported version"))

        self.request.data.update({'a_type': MULTIPLICATION})
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=False):
            result_data = {
                "inputs": self.request.data,
                "result": serializer.perform_operation()
                }
            return Response(result_data, status=status.HTTP_200_OK)
        else:
            # TODO: use a better status code?
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SimpleCalculatorView(APIView):
    """Wrapper over [SimpleCalculator][calcref] to perform math operations.

    [calcref]: https://github.com/badmetacoder/calculator
    """

    def post(self, *args, **kwrgs):
        """Using SimpleCalculator to get results of operations."""
        calc_instance = SimpleCalculator()
        expression = self.request.data.get('expression', None)
        if not expression:
            data = {"detail": _("'expression' is required.")}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # TODO: abstract this to a method.
        try:
            calc_instance.run(expression)
        except Exception as ex:  # TODO: better exception handling.
            msg = f"api called with '{expression}'\nAnd got an '{ex}' while executing."
            mail_admins('SimpleCalculator endpoint exception', msg)
            return Response(
                {"detail": _("Error with our logic while calculating your expression. "
                             "Admins have been notified.")},
                status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # TODO: better error handling from calc results
            if type(calc_instance.lcd) == str and 'Error' in calc_instance.lcd:
                error_data = {
                    'detail': _(f"Unable to produce result. "
                                f"Revise your expression: '{expression}' "
                                f"Place space between your numbers. ")
                    }
                return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                # in order to produce results, digits must be separated with spaces...
                result_data = {'inputs': expression, 'result': calc_instance.lcd}
                return Response(result_data, status=status.HTTP_200_OK)
