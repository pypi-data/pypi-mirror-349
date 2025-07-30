from unittest import TestCase

from solax_py_library.smart_scene.core.condition import DateCondition, BaseCondition


class TestCondition(TestCase):
    def test_condition(self):
        date_condition = DateCondition(
            update_value_function=lambda: 1,
        )
        assert isinstance(date_condition, BaseCondition)
