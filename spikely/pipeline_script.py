import spikeextractors as se
import spiketoolkit as st

################################ Extractors ###################################

# Create a toy example dataset (returns a recording extractor and sorting extractor)
recording, sorting_true= se.example_datasets.toy_example(duration=60)
print("Recording Extractor: " + str(recording))
print("Sorting Extractor: " + str(sorting_true) + '\n')

############################### Preprocessing #################################

# Filter recording extractor for the timeseries data (acts as a recording extractor that also filters!)
filter_recording = st.preprocessing.BandpassFilterRecording(recording, freq_min=300, freq_max=6000)
print("Filter Recording Extractor: " + str(filter_recording) + '\n')

################################### Sorting ###################################

#We have a string name for each sorter (we use that to get the class)
sorter_name = 'klusta'
output_folder='tmp_klusta'

#Fetch the sorter class corresponding to the sorter_name
SorterClass = st.sorters.sorter_dict[sorter_name]

#Instatiating the sorter class is generic (we always pass in these parameters)
sorter = SorterClass(recording=recording, output_folder=output_folder, grouping_property=None, parallel=False,
                     debug=False, delete_output_folder=False)
print("Sorter Class: " + str(sorter) + '\n')
#Get default params for specific sorter
params = SorterClass.default_params()

#set params for the sorter using default params
sorter.set_params(**params)
print("Default Params: "+ str(sorter.params) + '\n')

#Can update params by passing in the user entries
sorter.set_params(threshold_strong_std_factor=6, threshold_weak_std_factor=1)

#Run the sorter and save to the output file
sorter.run()

#Get a sorting object result from the output file
sorting_ms4 = sorter.get_result()
print("Sorting Extractor for ms4: " + str(sorting_ms4) + '\n')

################################ CURATION ###############################

# This is function call from the curation module, doesn't return anything (we support this)
st.postprocessing.export_to_phy(recording, sorting_ms4, output_folder='phy')
print("")

#Returns a sorting extractor object which has some curated results inside
curated_sorting = st.curation.ThresholdMinNumSpike(sorting_ms4, min_num_spike_threshold=120)
print("Curated Sorting Extractor: " + str(curated_sorting) + '\n')

#The curation gets rid of all units with less than 50 spikes
print("Original Units: " + str(sorting_ms4.get_unit_ids()))
print("Curated Units: " + str(curated_sorting.get_unit_ids()))
