from django.utils.translation import gettext as _
from django.core.mail import mail_admins

from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from calculator.simple import SimpleCalculator

from .serializers import OperationSerializer, ADDITION, MULTIPLICATION


class AdditionView(APIView):
    """Perform additions of multiple numbers.

    Arguments:
    `classification` (str): whether the operation is in real or imaginary numbers
    `values`(list): the list of values to be added.
    """

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
        serializer = OperationSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=False):
            result_data = {
                "inputs": self.request.data,
                "result": serializer.perform_operation()
                }
            return Response(result_data, status=status.HTTP_200_OK)
        else:
            # TODO: use a better status code?
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MultiplicationView(APIView):

    def post(self, *args, **kwargs):
        """"""
        # TODO: abstract versioning to a mixin?
        if self.request.version and self.request.version != '1':
            raise APIException(_("Unsuported version"))

        self.request.data.update({'a_type': MULTIPLICATION})
        serializer = OperationSerializer(data=self.request.data)
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
    """"""

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
