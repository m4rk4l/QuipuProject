from functools import reduce
import operator

from django.utils.translation import gettext as _

from rest_framework import serializers

ADDITION = 'addition'
MULTIPLICATION = 'multiplication'
OPERATIONS = (
    (ADDITION, _("Addition")),
    (MULTIPLICATION, _("Multiplication"))
)

REAL = 'real'
IMAGINARY = 'imaginary'
NUMBER_CLASSIFICATIONS = (
    (REAL, _("Real Numbers")),
    (IMAGINARY, _("Imaginary Numbers")),
)


class OperationSerializer(serializers.Serializer):
    """"""
    a_type = serializers.ChoiceField(choices=OPERATIONS)
    classification = serializers.ChoiceField(choices=NUMBER_CLASSIFICATIONS)
    values = serializers.ListField(child=serializers.FloatField())

    def validate(self, data):
        """"""
        classification = data['classification']
        values = data['values']
        if classification == IMAGINARY:
            if len(values) % 2 != 0:
                raise serializers.ValidationError(_("Provide an even list of numbers"))
        return data

    def perform_operation(self):
        """"""
        a_type = self.validated_data.get('a_type')
        classification = self.validated_data.get('classification')
        values = self.validated_data.get('values')

        if classification == REAL:
            if a_type == ADDITION:
                return f"{sum(values):6.2f}"
            elif a_type == MULTIPLICATION:
                return f"{reduce(operator.mul, values, 1):6.2f}"
        elif classification == IMAGINARY:
            complex_list = []
            value_iterator = iter(values)
            for n in value_iterator:
                complex_list.append(complex(n, next(value_iterator)))
            if a_type == ADDITION:
                return str(sum(complex_list))
            elif a_type == MULTIPLICATION:
                return str(reduce(operator.mul, complex_list, 1))
