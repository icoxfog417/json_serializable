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
    post = BlogPost("About Python", Category.technology, datetime.today(), "I learned about Python.")
    post_json = post.to_json()  # serialize the class object
    print("original:{0}".format(post))
    print("serialized:{0}".format(post_json))

    # deserialize
    another_post_json = '{"title": "About Todays Lunch", "category": 2, "date": "2014/1/1 12:00:00", "content":"I ate Sushi." }'
    another_post = BlogPost().load_json(another_post_json)
    print("deserialized:{0}".format(another_post))
