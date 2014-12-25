=================
Json Serializable
=================

 **Json Serializable** enables python class to be serializable/deserializable. ::

    json = your_class_obj.to_json()  # serialize
    obj = YourClass().load_json(json)  # deserialize


Quick Start
-----------

Sample code(see the `demo.py <https://github.com/icoxfog417/json_serializable/blob/master/test/demo.py>`_ file in test folder)::

    from enum import Enum
    from datetime import datetime
    from json_serializable import JsonSerializable


    class Category(Enum):
        technology = 1
        life = 2


    class BlogPost(JsonSerializable):

        def __init__(self, title="", category=Category.technology, date=None, content=""):
            super().__init__()
            self.title = title
            self.category = category
            self.date = date
            self.content = content

        def __str__(self):
            return "{0}@{1} [{2}]: {3}".format(self.title, self.date, self.category, self.content)

    if __name__ == "__main__":
        # serialize
        post = BlogPost("About Python", 
                        Category.technology,
                        datetime.today(),
                        "I learned about Python.")
        post_json = post.to_json()

        print("original:{0}".format(post))
        print("serialized:{0}".format(post_json))


        # deserialize
        another_post_json = '{"title": "About Todays Lunch", "category": 2, "date": "2014/1/1 12:00:00", "content":"I ate Sushi." }'
        another_post = BlogPost().load_json(another_post_json)

        print("deserialized:{0}".format(another_post))


The result is below::

    original:About Python@2014-12-25 14:48:35.960557 [Category.technology]: I learned about Python.
    serialized:{"__jsonserializable_type__": "__main__.BlogPost", "title": "About Python", "category": 1, "content": "I learned about Python.", "date": "2014-12-25 14:48:35"}

    deserialized:About Todays Lunch@2014/1/1 12:00:00 [Category.life]: I ate Sushi.

datetime and Enum also supported.

Customize
---------

You can customize serialize/deserialize rule like below.::

    self.set_serialize_rule(datetime, lambda v: v.strftime("%Y/%m/%d %H:%M:%S"))
    self.set_deserialize_rule(datetime, lambda t, v: datetime.strptime(v, "%Y/%m/%d %H:%M:%S"))

