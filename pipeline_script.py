import spikeextractors as se
import spiketoolkit as st
import os

# Create a toy example dataset
recording, sorting_true=se.example_datasets.toy_example(duration=60)
print(recording.getChannelIds())

# Filter extractor for the timeseries data
filter_recording = st.preprocessing.bandpass_filter(recording, freq_min=300, freq_max=6000)

'''Klusta spike sorter - This is the function call version, but we can talk about
the class based call where the parameters would be exposed.
'''
sorting_MS4 = st.sorters.run_mountainsort4(recording=recording, detect_sign=-1, adjacency_radius=-1,
                                           output_folder='tmp_MS4')

# You can use Phy to manually curate the sorting output of any spike sorter (this exports to that format)
st.postprocessing.exportToPhy(recording, sorting_MS4, output_folder='phy')
#Get rid of all units with less than 50 spikes
curated_sorting = st.postprocessing.threshold_min_num_spikes(sorting_MS4, min_num_spike_threshold=120)

print(sorting_MS4.getUnitIds())
print(curated_sorting.getUnitIds())
