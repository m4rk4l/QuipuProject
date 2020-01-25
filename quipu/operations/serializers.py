from django.utils.translation import gettext as _

from rest_framework import serializers


class AdditionSerializer(serializers.Serializer):
    """Addition serializer."""
    NATURAL = "natural"
    COMPLEX = "complex"
    SUPPORTED_ADDITION_TYPES = (
        (NATURAL, _("Natural Numbers")),
        (COMPLEX, _("Complex Numbers"))
    )

    addition_type = serializers.ChoiceField(choices=SUPPORTED_ADDITION_TYPES,
                                            allow_blank=False)
    values = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate(self, data):
        """Check wether we could add values depending on the addition_type."""

        addition_type = data['addition_type']
        values = data['values']
        if addition_type == self.COMPLEX:
            if len(values) % 2 != 0:
                raise serializers.ValidationError(_("Need to give provide an even list of numbers"))
        return data

    def perform_addition(self, *arg, **kwargs):
        """"""
        addition_type = self.validated_data.get('addition_type')
        values = self.validated_data.get('values')
        if addition_type == self.NATURAL:
            return sum(values)
        elif addition_type == self.COMPLEX:
            complex_list = []
            value_iterator = iter(values)
            for n in value_iterator:
                complex_list.append(complex(n, next(value_iterator)))
            return str(sum(complex_list))  # because Complex objects r not serializable.
