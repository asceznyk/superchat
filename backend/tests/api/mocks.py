class FakeRedis:

  def __init__(self):
    self.store = {}

  async def add_key_value(self, key, value):
    self.store[key] = value

  async def get_key_value(self, key):
    return self.store.get(key)

  async def delete_key_value(self, key):
    self.store.pop(key, None)

  async def does_key_exist(self, key):
    return key in self.store

