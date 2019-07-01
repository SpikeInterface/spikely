from .spike_element import SpikeElement


class Sorter(SpikeElement):
    """Preprocessor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.sorter_name)

    def run(self, input_payload, next_element):
        base_sorter_param_dict = {}
        base_sorter_param_dict['recording'] = input_payload

        params = self._params
        output_folder = params[0]
        parallel = params[1]
        base_sorter_param_dict[output_folder['name']] = output_folder['value']
        base_sorter_param_dict[parallel['name']] = parallel['value']
        sorter = self._interface_class(**base_sorter_param_dict)
        print(sorter.output_folders)

        sub_sorter_param_dict = {}
        for param in params[2:]:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            sub_sorter_param_dict[param_name] = param_value
        sorter.set_params(**sub_sorter_param_dict)
        sorter.run()
        print(output_folder['value'])
        return sorter.get_result(), sorter.output_folders[0]
