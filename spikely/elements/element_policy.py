from abc import ABC, abstractmethod


class ElementPolicy(ABC):

    def __init__(self, required_cls_list, cls_order_dict,
                 cls_display_name_dict):
        self._required_cls_list = required_cls_list
        self._cls_order_dict = cls_order_dict
        self._cls_display_name_dict = cls_display_name_dict

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

    def get_cls_display_name(self, cls):
        return self._cls_display_name_dict.get(cls, str(cls))
