class BaseCondition(object):
    def __init__(self, update_value_function, **kwargs):
        self.value = {}
        if not callable(update_value_function):
            raise ValueError("update_value_function must be callable")
        self.update_value_function = update_value_function

    def update_value(self):
        self.update_value_function()
        print(self.value)

    def meet_func(self, data, ctx):
        ...
