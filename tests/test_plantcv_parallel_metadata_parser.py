import pytest
from plantcv.parallel import check_date_range, convert_datetime_to_unixtime, metadata_parser, WorkflowConfig


def test_plantcv_parallel_metadata_parser_snapshots(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_snapshot_vis


def test_plantcv_parallel_metadata_parser_snapshots_coimg(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "FAKE"

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_snapshot_vis


@pytest.mark.parametrize("subdirs", [True, False])
def test_plantcv_parallel_metadata_parser_images(test_data, subdirs):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.flat_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014"
    config.end_date = "2014"
    config.timestampformat = '%Y'  # no date in filename so check date range and date_format are ignored
    config.imgformat = "jpg"
    config.include_all_subdirs = subdirs

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_flat_vis


def test_plantcv_parallel_metadata_parser_multivalue_filter(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.flat_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": ["VIS", "NIR"]}
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_flat_coprocess


def test_plantcv_parallel_metadata_parser_multivalue_filter_nomatch(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.flat_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": ["VIS", "PSII"]}
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_flat_vis


def test_plantcv_parallel_metadata_parser_regex(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.flat_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.delimiter = r'(VIS)_(SV)_(\d+)_(z1)_(h1)_(g0)_(e82)_(\d+)'

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_flat_vis


def test_plantcv_parallel_metadata_parser_images_outside_daterange(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.flat_imgdir_dates
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "timestamp"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "NIR"}
    config.start_date = "1970-01-01 00_00_00"
    config.end_date = "1970-01-01 00_00_00"
    config.timestampformat = "%Y-%m-%d %H_%M_%S"
    config.imgformat = "jpg"
    config.delimiter = r"(NIR)_(SV)_(\d)_(z1)_(h1)_(g0)_(e65)_(\d{4}-\d{2}-\d{2} \d{2}_\d{2}_\d{2})"

    meta = metadata_parser(config=config)
    assert meta == {}


def test_plantcv_parallel_metadata_parser_no_default_dates(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS", "camera": "SV", "id": "117770"}
    config.start_date = None
    config.end_date = None
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_snapshot_vis


def test_plantcv_parallel_check_date_range_wrongdateformat():
    start_date = 10
    end_date = 10
    img_time = '2010-10-10'

    with pytest.raises(SystemExit, match=r'does not match format'):
        date_format = '%Y%m%d'
        _ = check_date_range(start_date, end_date, img_time, date_format)


def test_plantcv_parallel_metadata_parser_snapshot_outside_daterange(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "1970-01-01 00:00:00.0"
    config.end_date = "1970-01-01 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"

    meta = metadata_parser(config=config)

    assert meta == {}


def test_plantcv_parallel_metadata_parser_fail_images(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"cartag": "VIS"}
    config.start_date = "1970-01-01 00:00:00.0"
    config.end_date = "1970-01-01 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)
    assert meta == test_data.metadata_snapshot_nir


def test_plantcv_parallel_metadata_parser_images_with_frame(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)

    assert meta == test_data.metadata_snapshot_coprocess


def test_plantcv_parallel_metadata_parser_images_no_frame(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "camera", "X", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)

    assert meta == test_data.metadata_snapshot_noframe


def test_plantcv_parallel_metadata_parser_images_no_camera(test_data):
    # Create config instance
    config = WorkflowConfig()
    config.input_dir = test_data.snapshot_imgdir
    config.json = "output.json"
    config.filename_metadata = ["imgtype", "X", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = test_data.workflow_script
    config.metadata_filters = {"imgtype": "VIS"}
    config.start_date = "2014-10-21 00:00:00.0"
    config.end_date = "2014-10-23 00:00:00.0"
    config.timestampformat = '%Y-%m-%d %H:%M:%S.%f'
    config.imgformat = "jpg"
    config.coprocess = "NIR"

    meta = metadata_parser(config=config)

    assert meta == test_data.metadata_snapshot_nocamera


def test_plantcv_parallel_convert_datetime_to_unixtime():
    unix_time = convert_datetime_to_unixtime(timestamp_str="1970-01-01", date_format="%Y-%m-%d")
    assert unix_time == 0


def test_plantcv_parallel_convert_datetime_to_unixtime_bad_strptime():
    with pytest.raises(SystemExit):
        _ = convert_datetime_to_unixtime(timestamp_str="1970-01-01", date_format="%Y-%m")
