from json_serializable import JsonSerializable
from test.test_class import print_title, SerializableClass
import unittest


class SerializeTestCase(unittest.TestCase):
    @print_title
    def test_from_json(self):
        target = SerializableClass()
        json_str = target.to_json()

        deserializer = SerializableClass(set_parameter=False)
        deserialized = deserializer.load_json(json_str)
        self.assertEqual(json_str, deserialized.to_json())

    @print_title
    def test_from_dict(self):
        target = SerializableClass()
        target_dict = target.__dict__

        deserializer = SerializableClass(set_parameter=False)
        deserialized = deserializer.load_dict(target_dict)

        self.assertEqual(target.to_json(), deserialized.to_json())

    def __deserialize(self):
        target = SerializableClass()
        json_str = target.to_json()

        deserializer = SerializableClass()
        deserialized = deserializer.load_json(json_str)

        return deserialized
