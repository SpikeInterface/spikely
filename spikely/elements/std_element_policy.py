from . import element_policy as sp_elp
from . import extractor as sp_ext
from . import sorter as sp_sor
from . import preprocessor as sp_pre


class StdElementPolicy(sp_elp.ElementPolicy):

    def __init__(self):
        a_required_cls_list = [
            sp_ext.Extractor, sp_sor.Sorter]

        a_cls_order_dict = {
            sp_ext.Extractor: 0, sp_pre.Preprocessor: 1,
            sp_sor.Sorter: 2}

        super().__init__(a_required_cls_list, a_cls_order_dict)

    def is_cls_selectable(self, cls):
        return cls in [
            sp_ext.Extractor, sp_pre.Preprocessor, sp_sor.Sorter]

    def is_cls_singleton(self, cls):
        return cls in [
            sp_ext.Extractor, sp_sor.Sorter]
