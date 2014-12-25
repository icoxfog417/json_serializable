from json_serializable import JsonSerializable
from test.test_class import print_title, SerializableClass
import json
import unittest


class SerializeTestCase(unittest.TestCase):

    @print_title
    def test_json_is_valid(self):
        loaded_json = json.loads(self.__serialize())
        print(loaded_json)
        self.assertTrue(loaded_json)

    @print_title
    def test_member(self):
        target = SerializableClass()
        loaded_json = json.loads(self.__serialize())
        self.assertEqual(loaded_json["number"], target.number)
        self.assertEqual(loaded_json["string"], target.string)

    @print_title
    def test_function_member(self):
        target = SerializableClass()
        loaded_json = json.loads(self.__serialize())
        self.assertEqual(loaded_json["getter"], target.getter())

    @print_title
    def test_enum(self):
        target = SerializableClass()
        loaded_json = json.loads(self.__serialize())
        self.assertEqual(loaded_json["selection"], target.selection.value)

    @print_title
    def test_object_member(self):
        target = SerializableClass()
        loaded_json = json.loads(self.__serialize())
        self. __validate_obj(target.obj, loaded_json["obj"])

    @print_title
    def test_object_list(self):
        target = SerializableClass()
        loaded_json = json.loads(self.__serialize())
        for index, item in enumerate(target.obj_list):
            self. __validate_obj(target.obj_list[index], loaded_json["obj_list"][index])

    def __validate_obj(self, target, dictionary):
        self.assertTrue(JsonSerializable.__JSON_SERIALIZABLE_TYPE_KEY__ in dictionary)
        self.assertEqual(dictionary["key"], target.key)
        self.assertEqual(dictionary["value"], target.value)

    def __serialize(self):
        target = SerializableClass()
        serialized = target.to_json()
        return serialized
