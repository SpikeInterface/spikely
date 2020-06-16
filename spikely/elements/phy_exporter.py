from spiketoolkit.postprocessing import export_to_phy


class PhyExporter:

    installed = True
    mode = "folder"

    @staticmethod
    def write_sorting(
        recording,
        sorting,
        save_path,
        compute_pc_features,
        compute_amplitudes,
        max_channels_per_template,
        **kwargs
    ):

        export_to_phy(
            recording,
            sorting,
            save_path,
            compute_pc_features=compute_pc_features,
            compute_amplitudes=compute_amplitudes,
            max_channels_per_template=max_channels_per_template,
            **kwargs
        )
