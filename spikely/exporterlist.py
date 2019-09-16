import spikeextractors as se
from .phy_exporter import PhyExporter

exporters_list = []
exporters_list.extend(se.extractorlist.writable_sorting_extractor_list)
exporters_list.append(PhyExporter)

se.sorting_exporter_dict

sorting_exporter_dict = se.sorting_exporter_dict
sorting_exporter_dict[PhyExporter.exporter_name] = PhyExporter
