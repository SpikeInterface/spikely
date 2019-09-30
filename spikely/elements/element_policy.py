from abc import ABC, abstractmethod


class ElementPolicy(ABC):

    def __init__(self, a_required_cls_list, a_cls_order_dict):
        self._required_cls_list = a_required_cls_list
        self._cls_order_dict = a_cls_order_dict

    @abstractmethod
    def is_cls_available(self, cls):
        pass

    @abstractmethod
    def is_cls_singleton(self, cls):
        pass

    @property
    def required_cls_list(self):
        return self._required_cls_list

    @property
    def cls_order_dict(self):
        return self._cls_order_dict
