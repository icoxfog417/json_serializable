import json
import inspect
from enum import Enum
from datetime import datetime


class JsonSerializable(object):
    __JSON_SERIALIZABLE_TYPE_KEY__ = "__jsonserializable_type__"

    def __init__(self):

        self.__serialize_rule = {}
        self.__serialize_rule.update({JsonSerializable: lambda j: j.__make_attribute_dict(True)})
        self.__serialize_rule.update({datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")})
        self.__serialize_rule.update({Enum: lambda v: v.value})

        self.__deserialize_rule = {}
        self.__deserialize_rule.update({datetime: lambda t, v: datetime.strptime(v, "%Y-%m-%d %H:%M:%S")})
        self.__deserialize_rule.update({Enum: lambda t, v: t(v)})

    def set_serialize_rule(self, target_type, rule):
        self.__serialize_rule.update({target_type: rule})

    def set_deserialize_rule(self, target_type, rule):
        self.__deserialize_rule.update({target_type: rule})

    @classmethod
    def load(cls, serialized):
        instance = cls()
        if isinstance(serialized, dict):
            return instance.load_dict(serialized)
        else:
            return instance.load_json(serialized)

    def load_dict(self, dictionary_data):
        if isinstance(dictionary_data, list):
            return list(map(lambda d: self.load_dict(d), dictionary_data))
        else:
            return self.__load_dict(dictionary_data)

    def load_json(self, json_str):
        dictionalized = json.loads(json_str)
        return self.load_dict(dictionalized)

    def __load_dict(self, data):

        def is_deseriarizable(judge_target):
            if isinstance(judge_target, dict) and self.__JSON_SERIALIZABLE_TYPE_KEY__ in judge_target:
                return True
            else:
                return False

        if is_deseriarizable(data):
            names = data[self.__JSON_SERIALIZABLE_TYPE_KEY__].split(".")
            class_name = names[len(names) - 1]
            package_name = data[self.__JSON_SERIALIZABLE_TYPE_KEY__].replace("." + class_name, "")

            mod = __import__(package_name, fromlist=[class_name])
            obj = getattr(mod, class_name)()

            load_data = dict(data)
            del load_data[self.__JSON_SERIALIZABLE_TYPE_KEY__]

            obj.__load_dict(load_data)
            return obj

        elif isinstance(data, list):
            list_field = []
            for d in data:
                list_field.append(self.__load_dict(d))

            return list_field

        elif isinstance(data, dict):
            attributes = self.__get_class_attributes(self)
            for key in data:
                attribute = [a for a in attributes if a[0] == key]
                if len(attribute) > 0:
                    self.__set_attribute(key, self.__load_dict(data[key]), getattr(self, key))

            return self

        else:
            return self.__attribute_to_value(data)

    def to_dict(self):
        dictionalized = self.__make_attribute_dict(self)
        return dictionalized

    def to_json(self):
        return json.dumps(self.to_dict())

    def __make_attribute_dict(self, instance):

        if isinstance(instance, JsonSerializable):
            attributes = self.__get_class_attributes(instance, True)
            attributes.append((self.__JSON_SERIALIZABLE_TYPE_KEY__, self.__get_full_name(instance)))

            attr_dict = {}
            for a in attributes:
                name = a[0]
                value = a[1]
                attr_dict[name] = self.__make_attribute_dict(value)

            return attr_dict

        elif isinstance(instance, dict):
            dict_field = []
            for key in instance:
                dict_field[key] = self.__make_attribute_dict(instance[key])

            return dict_field

        elif isinstance(instance, (list, tuple)):
            list_field = []
            for item in instance:
                list_field.append(self.__make_attribute_dict(item))

            return list_field

        else:
            return self.attribute_to_value(instance)

    @classmethod
    def __get_class_attributes(cls, instance, is_include_function=False):
        attributes = inspect.getmembers(instance, lambda a: not(inspect.isroutine(a)))

        # for getter method or function
        if is_include_function:
            attributes.extend(inspect.getmembers(instance, lambda a: inspect.isfunction(a)))

        # exclude private attribute
        return [a for a in attributes if not(a[0].startswith("_"))]

    @classmethod
    def __get_full_name(cls, instance):
        return instance.__module__ + "." + instance.__class__.__name__

    def __set_attribute(self, name, value, default_value):
        key_type = None
        rule_type = None
        for t in self.__deserialize_rule:
            if isinstance(default_value, t):
                key_type = t
                rule_type = default_value.__class__
                break

        if rule_type is not None and not isinstance(value, rule_type):
            setattr(self, name, self.__deserialize_rule[key_type](rule_type, value))
        else:
            setattr(self, name, value)

    def attribute_to_value(self, attribute):
        rule_type = None
        for t in self.__serialize_rule:
            if isinstance(attribute, t):
                rule_type = t
                break

        if rule_type is not None:
            return self.__serialize_rule[rule_type](attribute)
        else:
            return self.__attribute_to_value(attribute)

    @classmethod
    def __attribute_to_value(cls, attribute):
        if inspect.isfunction(attribute):
            return attribute()
        else:
            return attribute
