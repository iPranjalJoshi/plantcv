import pytest
import os
import json


class ParallelTestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "testdata")
        # plantcv.parallel.WorkflowConfig template file
        self.workflowconfig_template_file = os.path.join(self.datadir, "workflowconfig_template.json")
        # Flat image directory
        self.flat_imgdir = os.path.join(self.datadir, "flat_imgdir")
        # Flat image directory with dates in filenames
        self.flat_imgdir_dates = os.path.join(self.datadir, "images_w_date")
        # Snapshot image directory
        self.snapshot_imgdir = os.path.join(self.datadir, "snapshot_imgdir")
        # PlantCV workflow script
        self.workflow_script = os.path.join(self.datadir, "plantcv-script.py")
        # Output directory from parallel processing, contains results files
        self.parallel_results_dir = os.path.join(self.datadir, "parallel_results")
        # JSON results file with appended results
        self.appended_results_file = os.path.join(self.datadir, "appended_results.json")
        # JSON results file with a single set of results
        self.new_results_file = os.path.join(self.datadir, "new_results.json")
        # Valid JSON file but invalid results
        self.valid_json_file = os.path.join(self.datadir, "valid.json")
        # Metadata results for a VIS image from a snapshot directory
        self.metadata_snapshot_vis = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117770',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none'
                }
            }
        # Metadata results for an NIR image from a snapshot directory
        self.metadata_snapshot_nir = {
            'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
                'camera': 'SV',
                'imgtype': 'NIR',
                'zoom': 'z1',
                'exposure': 'e65',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117779',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none'
            }
        }
        # Metadata results for a VIS and NIR image pair from a snapshot directory
        self.metadata_snapshot_coprocess = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117770',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none',
                'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
            },
            'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
                'camera': 'SV',
                'imgtype': 'NIR',
                'zoom': 'z1',
                'exposure': 'e65',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117779',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none'
            }
        }
        # Metadata results for a VIS and NIR image pair without frame metadata from a snapshot directory
        self.metadata_snapshot_noframe = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': 'none',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117770',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none',
                'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
            },
            'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
                'camera': 'SV',
                'imgtype': 'NIR',
                'zoom': 'z1',
                'exposure': 'e65',
                'gain': 'g0',
                'frame': 'none',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117779',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none'
            }
        }
        # Metadata results for a VIS and NIR image pair without camera metadata from a snapshot directory
        self.metadata_snapshot_nocamera = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'none',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117770',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none',
                'coimg': 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'
            },
            'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
                'path': os.path.join(self.snapshot_imgdir, 'snapshot57383', 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
                'camera': 'none',
                'imgtype': 'NIR',
                'zoom': 'z1',
                'exposure': 'e65',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': '2014-10-22 17:49:35.187',
                'id': '117779',
                'plantbarcode': 'Ca031AA010564',
                'treatment': 'none',
                'cartag': '2143',
                'measurementlabel': 'C002ch_092214_biomass',
                'other': 'none'
            }
        }
        # Metadata for a VIS image from a flat directory
        self.metadata_flat_vis = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.flat_imgdir, 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': None,
                'id': '117770',
                'plantbarcode': 'none',
                'treatment': 'none',
                'cartag': 'none',
                'measurementlabel': 'none',
                'other': 'none'
            }
        }
        # Metadata for a VIS and NIR image pair from a flat directory
        self.metadata_flat_coprocess = {
            'VIS_SV_0_z1_h1_g0_e82_117770.jpg': {
                'path': os.path.join(self.flat_imgdir, 'VIS_SV_0_z1_h1_g0_e82_117770.jpg'),
                'camera': 'SV',
                'imgtype': 'VIS',
                'zoom': 'z1',
                'exposure': 'e82',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': None,
                'id': '117770',
                'plantbarcode': 'none',
                'treatment': 'none',
                'cartag': 'none',
                'measurementlabel': 'none',
                'other': 'none'
            },
            'NIR_SV_0_z1_h1_g0_e65_117779.jpg': {
                'path': os.path.join(self.flat_imgdir, 'NIR_SV_0_z1_h1_g0_e65_117779.jpg'),
                'camera': 'SV',
                'imgtype': 'NIR',
                'zoom': 'z1',
                'exposure': 'e65',
                'gain': 'g0',
                'frame': '0',
                'lifter': 'h1',
                'timestamp': None,
                'id': '117779',
                'plantbarcode': 'none',
                'treatment': 'none',
                'cartag': 'none',
                'measurementlabel': 'none',
                'other': 'none'
            }
        }
        # Metadata for an NIR image with subdaily timestamps
        self.metadata_flat_subdaily = {
            'NIR_SV_0_z1_h1_g0_e65_23_59_59.jpg': {
                'path': os.path.join(self.flat_imgdir_dates, 'NIR_SV_0_z1_h1_g0_e65_23_59_59.jpg'),
                'imgtype': 'NIR',
                'camera': 'SV',
                'frame': '0',
                'zoom': 'z1',
                'lifter': 'h1',
                'gain': 'g0',
                'exposure': 'e65',
                'timestamp': '23_59_59',
                'measurementlabel': 'none',
                'cartag': 'none',
                'id': 'none',
                'treatment': 'none',
                'plantbarcode': 'none',
                'other': 'none'
            }
        }

    @staticmethod
    def load_json(json_file):
        """JSON loader helper function.
        Inputs:
        json_file = JSON filepath

        Returns:
        data      = Dictionary of JSON data

        :param json_file: str
        :return data: dict
        """
        with open(json_file, "r") as fp:
            data = json.load(fp)
            return data

    def workflowconfig_template(self):
        """Load WorkflowConfig template from file."""
        return self.load_json(json_file=self.workflowconfig_template_file)

    def appended_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.appended_results_file)

    def new_results(self):
        """Load appended results from file."""
        return self.load_json(json_file=self.new_results_file)


@pytest.fixture(scope="session")
def parallel_test_data():
    """Test data object for the PlantCV parallel submodule."""
    return ParallelTestData()