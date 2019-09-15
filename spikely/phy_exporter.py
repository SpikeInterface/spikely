from spiketoolkit.postprocessing import export_to_phy
import numpy as np

class PhyExporter:

    exporter_name = 'PhyExporter'
    installed = True
    exporter_gui_params = [
        {'name': 'save_path', 'type': 'folder', 'title': "Save path"},
        {'name': 'nPC', 'type': 'int', 'value': 3, 'default': 3, 'title': "Number of principal components"},
        {'name': 'electrode_dimensions', 'type': 'int_list', 'value': None, 'default': None, 'title': "If electrode locations are 3D, it indicates the 2D dimensions to use as channel location."},
        {'name': 'grouping_property', 'type': 'str', 'value': None, 'default': None, 'title':
            "Property to group channels. E.g. if the recording extractor has the 'group' property and 'grouping_property' is 'group', then waveforms are computed group-wise."},
        {'name': 'ms_before', 'type': 'float', 'value': 1., 'default': 1., 'title': "Time period in ms to cut waveforms before the spike events."},
        {'name': 'ms_after', 'type': 'float', 'value': 2., 'default': 2., 'title': "Time period in ms to cut waveforms after the spike events."},
        {'name': 'dtype', 'type': 'np.dtype', 'value': None, 'default': None, 'title': "The dtype of underlying data (int16, float32, etc.)"},
        {'name': 'amp_method', 'type': 'str', 'value': 'absolute', 'default': 'absolute', 'title': "If 'absolute' (default), amplitudes are absolute amplitudes in uV are returned. If 'relative', amplitudes are returned as ratios between waveform amplitudes and template amplitudes."},
        {'name': 'amp_peak', 'type': 'str', 'value': 'both', 'default': 'both', 'title': "If maximum channel has to be found among negative peaks ('neg'), positive ('pos') or both ('both' - default)."},
        {'name': 'amp_frames_before', 'type': 'int', 'value': 3, 'default': 3, 'title': "Frames before peak to compute amplitude."},
        {'name': 'amp_frames_after', 'type': 'int', 'value': 3, 'default': 3, 'title': "Frames after peak to compute amplitude."},
        {'name': 'max_num_waveforms', 'type': 'int', 'value': float('inf'), 'default': float('inf'), 'title': "The maximum number of waveforms to extract. If 'inf', it will use all the waveforms."},
        {'name': 'max_num_pca_waveforms', 'type': 'int', 'value': float('inf'), 'default': float('inf'), 'title': "The maximum number of waveforms used to compute PCA. If 'inf', it will use all the waveforms."},
        {'name': 'write_waveforms', 'type': 'bool', 'value': False, 'default': False, 'title': "If True, waveforms are saved as waveforms.npy."},
        {'name': 'seed', 'type': 'int', 'value': 0, 'default': 0, 'title': "Random seed for extracting waveforms and pcs."},
    ]
    mode = 'folder'

    @staticmethod
    def write_sorting(recording, sorting, save_path, nPC=3, electrode_dimensions=None,
                      grouping_property=None, ms_before=1., ms_after=2., dtype=None, amp_method='absolute', amp_peak='both',
                      amp_frames_before=3, amp_frames_after=3, max_num_waveforms=np.inf, max_num_pca_waveforms=np.inf,
                      recompute_waveform_info=True, save_features_props=False, write_waveforms=False, verbose=False,
                      seed=0):

        export_to_phy(recording, sorting, save_path, nPC, electrode_dimensions,grouping_property, ms_before, ms_after, 
                      dtype, amp_method, amp_peak, amp_frames_before, amp_frames_after, max_num_waveforms, max_num_pca_waveforms,
                      recompute_waveform_info, save_features_props, write_waveforms, verbose, seed)