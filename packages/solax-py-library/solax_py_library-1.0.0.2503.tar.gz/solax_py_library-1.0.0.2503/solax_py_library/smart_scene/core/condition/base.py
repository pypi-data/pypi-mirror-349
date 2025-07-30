class BaseCondition(object):
    def __init__(self, **kwargs):
        self.value = {}

    def update_value(self):
        ...

    def meet_func(self, data, ctx):
        ...
