from django.test import TestCase

from .. import serializers


class TestOperationSerializer(TestCase):
    """"""

    def setUp(self, *args, **kwargs):
        """"""

    def test_invalid_addition_imaginary_with_odd_values(self):
        """Check that validation fails if odd amount of values given in Serializer"""
        data = {
            "a_type": serializers.ADDITION,
            "classification": serializers.IMAGINARY,
            "values": [-1, 2, -3]
            }
        a_serializer = serializers.OperationSerializer(data=data)
        self.assertFalse(a_serializer.is_valid(raise_exception=False))
        has_errors = len(a_serializer.errors) > 0
        self.assertTrue(has_errors)

    def test_valid_addition_imaginary_with_even_values(self):
        """Check for successful operations on complex values."""
        data = {
            "a_type": serializers.ADDITION,
            "classification": serializers.IMAGINARY,
            "values": [-1, 2, 3, -4]
            }
        a_serializer = serializers.OperationSerializer(data=data)
        self.assertTrue(a_serializer.is_valid(raise_exception=False))
        has_errors = len(a_serializer.errors) > 0
        self.assertFalse(has_errors)
        result = a_serializer.perform_operation()
        expected_complex = complex(2, -2)
        self.assertEqual(result, expected_complex)

    def test_valid_real_addition(self):
        """"""
        data = {
            "a_type": serializers.ADDITION,
            "classification": serializers.IMAGINARY,
            "values": [-1, 2, 3, -4]
            }
        a_serializer = serializers.OperationSerializer(data=data)
        self.assertTrue(a_serializer.is_valid(raise_exception=False))
        result = a_serializer.perform_operation()
        self.assertEqual(result, 0)
