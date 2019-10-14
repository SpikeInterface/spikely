from . import element_policy as sp_elp
from . import recording_extractor as sp_ree
from . import sorter as sp_sor
from . import preprocessor as sp_pre
from . import curator as sp_cur
from . import sorting_exporter as sp_soe


class StdElementPolicy(sp_elp.ElementPolicy):

    def __init__(self):
        required_cls_list = [
            sp_ree.RecordingExtractor, sp_sor.Sorter]

        cls_order_dict = {
            sp_ree.RecordingExtractor: 0, sp_pre.Preprocessor: 1,
            sp_sor.Sorter: 2, sp_cur.Curator: 3, sp_soe.SortingExporter: 4}

        cls_display_name_dict = {
            sp_ree.RecordingExtractor: 'Recording Extractor',
            sp_pre.Preprocessor: 'Preprocessor',
            sp_sor.Sorter: 'Sorter', sp_cur.Curator: 'Curator',
            sp_soe.SortingExporter: 'Sorting Exporter'}

        super().__init__(required_cls_list, cls_order_dict,
                         cls_display_name_dict)

    def is_cls_available(self, cls):
        return cls in [
            sp_ree.RecordingExtractor, sp_pre.Preprocessor, sp_sor.Sorter,
            sp_cur.Curator, sp_soe.SortingExporter]

    def is_cls_singleton(self, cls):
        return cls in [
            sp_ree.RecordingExtractor, sp_sor.Sorter, sp_soe.SortingExporter]
