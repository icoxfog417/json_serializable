from json_serializable import JsonSerializable
from datetime import datetime
from enum import Enum


class SerializableClass(JsonSerializable):

    def __init__(self, set_parameter=True):
        super(SerializableClass, self).__init__()

        self.getter = lambda: self.__private
        self.set_serialize_rule(datetime, lambda v: v.strftime("%Y/%m/%d %H:%M:%S"))
        self.set_deserialize_rule(datetime, lambda t, v: datetime.strptime(v, "%Y/%m/%d %H:%M:%S"))

        if set_parameter:
            self.__set_parameters()
        else:
            self.__init_parameters()

    def __set_parameters(self):
        self.number = 100
        self.string = "XXX"

        self.__private = 10
        self.selection = Selection.option2

        self.list = [10, 11, 12]
        self.tuple = ("A", "B", "C")

        self.date = datetime.today()
        self.obj = SerialiableKeyValue("A", "100")
        self.obj_list = list(map(lambda key: SerialiableKeyValue(key, ord(key)), ("A", "B", "C")))
        self.nested_list = ["A", ["B", "C"]]
        self.nested_obj_list = [SerialiableKeyValue("A", 100), [SerialiableKeyValue("B", 200), SerialiableKeyValue("C", 300)]]

    def __init_parameters(self):
        self.number = 0
        self.string = ""

        self.__private = 10
        self.selection = Selection.option1

        self.list = []
        self.tuple = ()

        self.date = datetime(1000, 1, 1)
        self.obj = SerialiableKeyValue()
        self.obj_list = [SerialiableKeyValue()]
        self.nested_list = [[]]
        self.nested_obj_list = [[SerialiableKeyValue()]]


class SerialiableKeyValue(JsonSerializable):

    def __init__(self, key=None, value=None):
        super(SerialiableKeyValue, self).__init__()
        self.key = key
        self.value = value


class Selection(Enum):
    option1 = 1
    option2 = 2
    option3 = 3


def print_title(test_case):

    def wrapper(*args, **kwargs):
        print("@" + test_case.__name__ + "-------------------------------------------")
        return test_case(*args, **kwargs)

    return wrapper
