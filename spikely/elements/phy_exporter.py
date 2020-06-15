from spiketoolkit.postprocessing import export_to_phy
import numpy as np

class PhyExporter:

    installed = True
    mode = 'folder'

    @staticmethod
    def write_sorting(recording, sorting, save_path, n_comp=3, electrode_dimensions=None,
                      grouping_property=None, ms_before=1., ms_after=2., dtype=None, amp_method='absolute', amp_peak='both',
                      amp_frames_before=3, amp_frames_after=3, max_spikes_for_pca=100000,
                      recompute_info=True, save_features_props=False, write_waveforms=False, verbose=False,
                      seed=0):

        export_to_phy(recording, sorting, save_path, n_comp, electrode_dimensions,
                      grouping_property, ms_before, ms_after, dtype, amp_method, amp_peak,
                      amp_frames_before, amp_frames_after, max_spikes_for_pca,
                      recompute_info, save_features_props, write_waveforms, verbose,
                      seed)
