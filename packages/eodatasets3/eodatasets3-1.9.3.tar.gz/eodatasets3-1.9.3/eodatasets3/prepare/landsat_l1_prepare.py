"""
Prepare eo3 metadata for USGS Landsat Level 1 data.

Input dataset paths can be directories or tar files.
"""

import logging
import os
import re
import tarfile
import uuid
from collections.abc import Callable, Generator, Iterable
from datetime import datetime, timezone
from pathlib import Path

import click
import rasterio

from eodatasets3 import DatasetPrepare, serialise, utils
from eodatasets3.properties import FileFormat
from eodatasets3.ui import PathPath

_COPYABLE_MTL_FIELDS = {}
_COPYABLE_MTL_FIELDS["C1"] = [
    (
        "metadata_file_info",
        (
            "landsat_scene_id",
            "landsat_product_id",
            "station_id",
            "processing_software_version",
        ),
    ),
    (
        "product_metadata",
        ("data_type", "ephemeris_type", "wrs_path", "wrs_row", "collection_category"),
    ),
    (
        "image_attributes",
        (
            "ground_control_points_version",
            "ground_control_points_model",
            "geometric_rmse_model_x",
            "geometric_rmse_model_y",
            "ground_control_points_verify",
            "geometric_rmse_verify",
        ),
    ),
    ("projection_parameters", ("scan_gap_interpolation",)),
]
_COPYABLE_MTL_FIELDS["C2"] = [
    (
        "level2_processing_record",
        (
            "landsat_scene_id",
            "landsat_product_id",
            "processing_software_version",
            "algorithm_source_surface_reflectance",
            "collection_category",
            "ground_control_points_version",
            "ground_control_points_model",
            "geometric_rmse_model_x",
            "geometric_rmse_model_y",
        ),
    ),
    (
        "level1_processing_record",
        (
            "landsat_scene_id",
            "landsat_product_id",
            "processing_software_version",
            "collection_category",
            "ground_control_points_version",
            "ground_control_points_model",
            "geometric_rmse_model_x",
            "geometric_rmse_model_y",
        ),
    ),
    (
        "image_attributes",
        (
            "station_id",
            "wrs_path",
            "wrs_row",
            # "ground_control_points_verify",  # not in the test data for C1 or C2
            # "geometric_rmse_verify",   # not in the test data for C1 or C2
        ),
    ),
    # not in the test data for C1 or C2
    # ("level1_projection_parameters", ("scan_gap_interpolation",)),
]

# Static namespace to generate uuids for datacube indexing
USGS_UUID_NAMESPACE = uuid.UUID("276af61d-99f8-4aa3-b2fb-d7df68c5e28f")

LANDSAT_OLI_TIRS_BAND_ALIASES = {
    "band_1": "coastal_aerosol",
    "band_2": "blue",
    "band_3": "green",
    "band_4": "red",
    "band_5": "nir",
    "band_6": "swir_1",
    "band_7": "swir_2",
    "band_8": "panchromatic",
    "band_9": "cirrus",
    "band_st_b10": "lwir",  # USGS only
    "band_10": "lwir_1",
    "band_11": "lwir_2",
    "quality_l1_pixel": "quality",
    # Older collection called quality a "band"
    "band_quality": "quality",
    "qa_aerosol": "qa_aerosol",
    "thermal_radiance": "thermal_radiance",
    "upwell_radiance": "upwell_radiance",
    "downwell_radiance": "downwell_radiance",
    "atmospheric_transmittance": "atmos_transmittance",
    "atmospheric_opacity": "atmos_opacity",
    "emissivity": "emissivity",
    "emissivity_stdev": "emissivity_stdev",
    "cloud_distance": "cloud_distance",
    "quality_l2_aerosol": "qa_aerosol",
    "quality_l2_surface_reflectance_cloud": "qa_cloud",
    "quality_l2_surface_temperature": "qa_temperature",
    "quality_l1_radiometric_saturation": "qa_radsat",
    "angle_sensor_azimuth_band_4": "view_azimuth",
    "angle_sensor_zenith_band_4": "view_zenith",
    "angle_solar_azimuth_band_4": "solar_azimuth",
    "angle_solar_zenith_band_4": "solar_zenith",
}

LANDSAT_xTM_BAND_ALIASES = {
    "band_1": "blue",
    "band_2": "green",
    "band_3": "red",
    "band_4": "nir",
    "band_5": "swir_1",
    "band_6": "tir",
    "band_6_vcid_1": "tir_1",
    "band_6_vcid_2": "tir_2",
    "band_st_b6": "lwir",  # USGS only
    "band_7": "swir_2",
    "band_8": "panchromatic",
    "band_quality": "quality",
    "quality_l1_pixel": "quality",
    "cloud_qa": "qa_cloud",
    "quality_l1_radiometric_saturation": "qa_radsat",
    "quality_l2_aerosol": "qa_aerosol",
    "quality_l2_surface_reflectance_cloud": "qa_cloud",
    "quality_l2_surface_temperature": "qa_temperature",
    "thermal_radiance": "thermal_radiance",
    "upwell_radiance": "upwell_radiance",
    "downwell_radiance": "downwell_radiance",
    "atmospheric_transmittance": "atmos_transmittance",
    "atmospheric_opacity": "atmos_opacity",
    "emissivity": "emissivity",
    "emissivity_stdev": "emissivity_stdev",
    "cloud_distance": "cloud_distance",
    "angle_sensor_azimuth_band_4": "view_azimuth",
    "angle_sensor_zenith_band_4": "view_zenith",
    "angle_solar_azimuth_band_4": "solar_azimuth",
    "angle_solar_zenith_band_4": "solar_zenith",
}

MTL_PAIRS_RE = re.compile(r"(\w+)\s=\s(.*)")

LANDSAT_MTL_MAP = {
    "C1": {
        "product_contents_cn": "metadata_file_info",
        "product_contents_of": "product_metadata",
        "product_contents_fn": "product_metadata",
        "image_attributes": "product_metadata",
        "level1_processing_record": "metadata_file_info",
        "level1_projection_parameters": "projection_parameters",
    },
    "C2": {
        "product_contents_cn": "product_contents",
        "product_contents_of": [
            "level2_processing_record",
            "level1_processing_record",
        ],
        "product_contents_fn": "product_contents",
        "image_attributes": "image_attributes",
        "leveln_processing_record": [
            "level2_processing_record",
            "level1_processing_record",
        ],
        "leveln_projection_parameters": [
            "projection_attributes",
            "level2_projection_parameters",
            "level1_projection_parameters",
        ],
    },
}


def get_band_alias_mappings(sat: str, instrument: str) -> dict[str, str]:
    """
    To load the band_names for referencing either LANDSAT8 or LANDSAT7 or LANDSAT5 bands
    Landsat7 and Landsat5 have same band names

    >>> get_band_alias_mappings('landsat-8', 'OLI_TIRS') == LANDSAT_OLI_TIRS_BAND_ALIASES
    True
    >>> get_band_alias_mappings('landsat-8', 'OLI') == LANDSAT_OLI_TIRS_BAND_ALIASES
    True
    >>> get_band_alias_mappings('landsat-5', 'TM') == LANDSAT_xTM_BAND_ALIASES
    True
    >>> get_band_alias_mappings('landsat-5', 'TM') == LANDSAT_xTM_BAND_ALIASES
    True
    >>> get_band_alias_mappings('aqua', 'MODIS') == LANDSAT_xTM_BAND_ALIASES
    Traceback (most recent call last):
    ...
    NotImplementedError: Unexpected satellite. Only landsat handled currently. Got 'aqua'
    >>> get_band_alias_mappings('landsat-5', 'MSS') == LANDSAT_xTM_BAND_ALIASES
    Traceback (most recent call last):
    ...
    NotImplementedError: Landsat version not yet supported: 'landsat-5', 'MSS'
    """

    if not sat.startswith("landsat-"):
        raise NotImplementedError(
            f"Unexpected satellite. Only landsat handled currently. Got {sat!r}"
        )
    landsat_number = int(sat.split("-")[1])

    if landsat_number in (8, 9):
        return LANDSAT_OLI_TIRS_BAND_ALIASES
    if landsat_number in (4, 5, 7) and instrument.endswith("TM"):
        return LANDSAT_xTM_BAND_ALIASES

    raise NotImplementedError(
        f"Landsat version not yet supported: {sat!r}, {instrument!r}"
    )


def get_mtl_content(acquisition_path: Path, root_element=None) -> tuple[dict, str, str]:
    """
    Find MTL file for the given path. It could be a directory or a tar file.

    It will return the MTL parsed as a dict and its filename.
    """

    def iter_tar_members(tp: tarfile.TarFile) -> Generator[tarfile.TarInfo, None, None]:
        """
        This is a lazy alternative to TarInfo.getmembers() that only reads one tar item at a time.

        We're reading the MTL file, which is almost always the first entry in the tar, and then
        closing it, so we're avoiding skipping through the entirety of the tar.
        """
        member = tp.next()
        while member is not None:
            yield member
            member = tp.next()

    if not acquisition_path.exists():
        raise RuntimeError(f"Missing path '{acquisition_path}'")

    if acquisition_path.is_file() and tarfile.is_tarfile(str(acquisition_path)):
        with tarfile.open(str(acquisition_path), "r") as tp:
            for member in iter_tar_members(tp):
                if "_MTL.txt" in member.name:
                    with tp.extractfile(member) as fp:
                        mtl_doc, file_root_element = read_mtl(fp)
                        return mtl_doc, file_root_element, member.name
            else:
                raise RuntimeError(f"MTL file not found in {acquisition_path!s}")

    else:
        paths = list(acquisition_path.rglob("*_MTL.txt"))
        if not paths:
            raise RuntimeError("No MTL file")
        if len(paths) > 1:
            raise RuntimeError(
                f"Multiple MTL files found in given acq path {acquisition_path}"
            )
        [path] = paths
        with path.open("r") as fp:
            mtl_doc, file_root_element = read_mtl(fp, root_element)
            return mtl_doc, file_root_element, path.name


def read_mtl(fp: Iterable[str | bytes], root_element=None) -> tuple[dict, str]:
    def _parse_value(s: str) -> int | float | str:
        """
        >>> _parse_value("asdf")
        'asdf'
        >>> _parse_value("123")
        123
        >>> _parse_value("3.14")
        3.14
        """
        s = s.strip('"')
        for parser in [int, float]:
            try:
                return parser(s)
            except ValueError:
                pass
        return s

    def _parse_group(
        lines: Iterable[str | bytes],
        key_transform: Callable[[str], str] = lambda s: s.lower(),
    ) -> dict:
        tree = {}
        for line in lines:
            # If line is bytes-like convert to str
            if isinstance(line, bytes):
                line = line.decode("utf-8")
            match = MTL_PAIRS_RE.findall(line)
            if match:
                key, value = match[0]
                if key == "GROUP":
                    tree[key_transform(value)] = _parse_group(lines)
                elif key == "END_GROUP":
                    break
                else:
                    tree[key_transform(key)] = _parse_value(value)
        return tree

    tree = _parse_group(fp)
    if root_element is None:
        root_element = next(iter(tree.keys()))
    return tree[root_element], root_element


def _iter_image_paths(product_doc: dict) -> Generator[tuple[str, str], None, None]:
    file_pattern = re.compile(r"file_name_([\w]+)")
    for name, filepath in product_doc.items():
        match = file_pattern.match(name)
        if not match or not filepath.endswith(".TIF"):
            continue

        file_id = match.groups()[0]
        yield file_id, filepath


def prepare_and_write(
    ds_path: Path,
    output_yaml_path: Path,
    source_telemetry: Path | None = None,
    # TODO: Can we infer producer automatically? This is bound to cause mistakes othewise
    producer="usgs.gov",
    embed_location: bool = False,
) -> tuple[uuid.UUID, Path]:
    """
    Prepare an eo3 metadata file for a Level1 dataset.

    Input dataset path can be a folder or a tar file.
    """
    mtl_doc, root_element, mtl_filename = get_mtl_content(ds_path)
    if not mtl_doc:
        raise ValueError(f"No MTL file found for {ds_path}")
    collection_key = "C2" if root_element == "landsat_metadata_file" else "C1"
    leveln_key_prefix = "leveln" if collection_key == "C2" else "level1"
    coll_map = LANDSAT_MTL_MAP[collection_key]
    usgs_collection_number = mtl_doc[coll_map["product_contents_cn"]].get(
        "collection_number"
    )
    if usgs_collection_number is None:
        raise NotImplementedError(
            "Dataset has no collection number: pre-collection data is not supported."
        )

    data_format = None
    if isinstance(coll_map["product_contents_of"], list):
        for leveln in coll_map["product_contents_of"]:
            if leveln in mtl_doc:
                data_format = mtl_doc[leveln]["output_format"]
                break
    else:
        data_format = mtl_doc[coll_map["product_contents_of"]]["output_format"]
    if data_format.upper() != "GEOTIFF":
        raise NotImplementedError(f"Only GTiff currently supported, got {data_format}")
    file_format = FileFormat.GeoTIFF

    # Assumed below.
    projection_params = None
    if isinstance(coll_map[leveln_key_prefix + "_projection_parameters"], list):
        for leveln in coll_map[leveln_key_prefix + "_projection_parameters"]:
            if leveln in mtl_doc:
                projection_params = mtl_doc[leveln]
                break
    else:
        projection_params = mtl_doc[
            coll_map[leveln_key_prefix + "_projection_parameters"]
        ]
    if (
        "grid_cell_size_thermal" in projection_params
        and "grid_cell_size_reflective" in projection_params
        and (
            projection_params["grid_cell_size_reflective"]
            != projection_params["grid_cell_size_thermal"]
        )
    ):
        raise NotImplementedError("reflective and thermal have different cell sizes")
    ground_sample_distance = min(
        value
        for name, value in projection_params.items()
        if name.startswith("grid_cell_size_")
    )

    leveln_product_id = None
    leveln_processed = None
    leveln_landsat_data_type = None
    if isinstance(coll_map[leveln_key_prefix + "_processing_record"], list):
        for leveln in coll_map[leveln_key_prefix + "_processing_record"]:
            if leveln in mtl_doc:
                leveln_product_id = mtl_doc[leveln]["landsat_product_id"]
                leveln_processed = mtl_doc[leveln]["date_product_generated"]
                leveln_landsat_data_type = mtl_doc[leveln]["processing_level"]
                break
    else:
        leveln_product_id = mtl_doc[coll_map[leveln_key_prefix + "_processing_record"]][
            "landsat_product_id"
        ]
        leveln_processed = mtl_doc[coll_map[leveln_key_prefix + "_processing_record"]][
            "file_date"
        ]  # for C1 only
        leveln_landsat_data_type = mtl_doc[coll_map["product_contents_of"]]["data_type"]

    with DatasetPrepare(
        metadata_path=output_yaml_path,
        dataset_location=ds_path,
        # Detministic ID based on USGS's product id (which changes when the scene is reprocessed by them)
        dataset_id=uuid.uuid5(USGS_UUID_NAMESPACE, leveln_product_id),
        naming_conventions="dea",
    ) as p:
        if source_telemetry:
            if producer != "ga.gov.au":
                raise NotImplementedError(
                    "Only GA's L1 data is expected to have telemetry source data?"
                )
            p.add_source_path(source_telemetry)

        p.platform = mtl_doc[coll_map["image_attributes"]]["spacecraft_id"]
        p.instrument = mtl_doc[coll_map["image_attributes"]]["sensor_id"]
        p.product_family = "level" + leveln_landsat_data_type[1]
        p.producer = producer
        p.datetime = "{}T{}".format(
            mtl_doc[coll_map["image_attributes"]]["date_acquired"],
            mtl_doc[coll_map["image_attributes"]]["scene_center_time"],
        )
        p.processed = leveln_processed
        if collection_key == "C2":
            p.properties["landsat:data_type"] = leveln_landsat_data_type
        p.properties["odc:file_format"] = file_format
        p.properties["eo:gsd"] = ground_sample_distance
        cloud_cover = mtl_doc["image_attributes"]["cloud_cover"]
        # Cloud cover is -1 when missing (such as TIRS-only data)
        if cloud_cover != -1:
            p.properties["eo:cloud_cover"] = cloud_cover
        p.properties["eo:sun_azimuth"] = mtl_doc["image_attributes"]["sun_azimuth"]
        p.properties["eo:sun_elevation"] = mtl_doc["image_attributes"]["sun_elevation"]
        p.properties["landsat:collection_number"] = usgs_collection_number
        for section, fields in _COPYABLE_MTL_FIELDS[collection_key]:
            if section in mtl_doc:
                for field in fields:
                    value = mtl_doc[section].get(field)
                    if (
                        value is not None
                        and p.properties.get(f"landsat:{field}") is None
                    ):
                        p.properties[f"landsat:{field}"] = value

        p.region_code = f"{p.properties['landsat:wrs_path']:03d}{p.properties['landsat:wrs_row']:03d}"
        org_collection_number = utils.get_collection_number(
            p.platform, p.producer, p.properties["landsat:collection_number"]
        )
        p.dataset_version = f"{org_collection_number}.0.{p.processed:%Y%m%d}"

        # NRT product?
        # Category is one of: T1, T2 or RT ('real time')
        if p.properties["landsat:collection_category"] == "RT":
            p.properties["dea:dataset_maturity"] = "nrt"

        band_aliases = get_band_alias_mappings(p.platform, p.instrument)

        for usgs_file_type, file_location in _iter_image_paths(
            mtl_doc[coll_map["product_contents_fn"]]
        ):
            if usgs_file_type not in band_aliases:
                all_found = dict(
                    _iter_image_paths(mtl_doc[coll_map["product_contents_fn"]])
                )
                raise ValueError(
                    f"Band name {usgs_file_type!r} is not known among our aliases. "
                    f"(All bands found in the dataset: {all_found!r})"
                )
            p.note_measurement(
                band_aliases[usgs_file_type],
                file_location,
                relative_to_dataset_location=True,
                expand_valid_data=(
                    usgs_file_type.startswith("band_")
                    and (
                        # The older collection called quality a "band"
                        "quality" not in usgs_file_type
                    )
                ),
            )

        p.note_accessory_file("metadata:landsat_mtl", Path(mtl_filename))
        return p.done(embed_location=embed_location)


@click.command(help=__doc__)
@click.option(
    "--output-base",
    help="Write metadata files into a directory instead of alongside each dataset",
    required=False,
    type=PathPath(exists=True, writable=True, dir_okay=True, file_okay=False),
)
@click.option(
    "--source",
    "source_telemetry",
    help="Path to the source telemetry data for all of the provided datasets"
    "(either the folder or metadata file)",
    required=False,
    type=PathPath(exists=True),
)
@click.option(
    "--embed-location/--no-embed-location",
    is_flag=True,
    help="Embed the location of the dataset in the metadata "
    "(if you wish to store them separately)",
)
@click.option(
    "--producer",
    help="Organisation that produced the data: probably either 'ga.gov.au' or 'usgs.gov'.",
    required=False,
    default="usgs.gov",
)
@click.argument(
    "datasets", type=PathPath(exists=True, readable=True, writable=False), nargs=-1
)
@click.option(
    "--overwrite-existing/--skip-existing",
    is_flag=True,
    default=False,
    help="Overwrite if exists (otherwise skip)",
)
@click.option(
    "--newer-than",
    type=serialise.ClickDatetime(),
    default=None,
    help="Only process files newer than this date",
)
def main(
    output_base: Path | None,
    datasets: list[Path],
    overwrite_existing: bool,
    producer: str,
    embed_location: bool,
    source_telemetry: Path | None,
    newer_than: datetime | None,
):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO
    )
    with rasterio.Env():
        for ds in datasets:
            if output_base:
                output = output_base.absolute().joinpath(
                    *utils.subfolderise(_dataset_region_code(ds))
                )
                output.mkdir(parents=True, exist_ok=True)
            else:
                # Alongside the dataset itself.
                output = ds.absolute().parent

            ds_path = _normalise_dataset_path(Path(ds).absolute())
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(ds)
            create_date = datetime.fromtimestamp(ctime, timezone.utc)
            if newer_than and (create_date <= newer_than):
                logging.info(
                    "Creation time %s older than start date %s ...SKIPPING %s",
                    newer_than - create_date,
                    newer_than,
                    ds_path.name,
                )
                continue

            logging.info("Processing %s", ds_path)
            output_yaml = output / f"{_dataset_name(ds_path)}.odc-metadata.yaml"

            if output_yaml.exists():
                if not overwrite_existing:
                    logging.info("Output exists: skipping. %s", output_yaml)
                    continue

                logging.info("Output exists: overwriting %s", output_yaml)

            output_uuid, output_path = prepare_and_write(
                ds_path,
                output_yaml,
                producer=producer,
                source_telemetry=source_telemetry,
                embed_location=embed_location,
            )
            logging.info("Wrote dataset %s to %s", output_uuid, output_path)


def _normalise_dataset_path(input_path: Path) -> Path:
    """
    Dataset path should be either the direct imagery folder (mtl+bands) or a tar path.

    Translate other inputs (example: the MTL path) to one of the two.

    >>> import tempfile
    >>> tmppath = Path(tempfile.mkdtemp())
    >>> ds_path = tmppath.joinpath('LE07_L1GT_104078_20131209_20161119_01_T1')
    >>> ds_path.mkdir()
    >>> mtl_path = ds_path / 'LC08_L1TP_090084_20160121_20170405_01_T1_MTL.txt'
    >>> mtl_path.write_text('<mtl content>')
    13
    >>> _normalise_dataset_path(ds_path).relative_to(tmppath).as_posix()
    'LE07_L1GT_104078_20131209_20161119_01_T1'
    >>> _normalise_dataset_path(mtl_path).relative_to(tmppath).as_posix()
    'LE07_L1GT_104078_20131209_20161119_01_T1'
    >>> tar_path = tmppath / 'LS_L1GT.tar.gz'
    >>> tar_path.write_text('fake tar')
    8
    >>> _normalise_dataset_path(tar_path).relative_to(tmppath).as_posix()
    'LS_L1GT.tar.gz'
    >>> _normalise_dataset_path(Path(tempfile.mkdtemp()))
    Traceback (most recent call last):
    ...
    ValueError: No MTL files within input path .... Not a dataset?
    """
    input_path = normalise_nci_symlinks(input_path)
    if input_path.is_file():
        if ".tar" in input_path.suffixes:
            return input_path
        input_path = input_path.parent

    mtl_files = list(input_path.rglob("*_MTL.txt"))

    if not mtl_files:
        raise ValueError(
            f"No MTL files within input path '{input_path}'. Not a dataset?"
        )
    if len(mtl_files) > 1:
        raise ValueError(
            f"Multiple MTL files in a single dataset (got path: {input_path})"
        )
    return input_path


def normalise_nci_symlinks(input_path: Path) -> Path:
    """
    If it's an NCI lustre path, always use the symlink (`/g/data`) rather than specific drives (eg. `/g/data2`).

    >>> normalise_nci_symlinks(Path('/g/data2/v10/some/dataset.tar')).as_posix()
    '/g/data/v10/some/dataset.tar'
    >>> normalise_nci_symlinks(Path('/g/data1a/v10/some/dataset.tar')).as_posix()
    '/g/data/v10/some/dataset.tar'
    >>> # Don't change other paths!
    >>> normalise_nci_symlinks(Path('/g/data/v10/some/dataset.tar')).as_posix()
    '/g/data/v10/some/dataset.tar'
    >>> normalise_nci_symlinks(Path('/Users/testuser/unrelated-path.yaml')).as_posix()
    '/Users/testuser/unrelated-path.yaml'
    """
    match = re.match(r"^/g/data[0-9a-z]+/(.*)", str(input_path))
    if not match:
        return input_path

    [offset] = match.groups()
    return Path("/g/data/" + offset)


def _dataset_name(ds_path: Path) -> str:
    """
    >>> _dataset_name(Path("example/LE07_L1GT_104078_20131209_20161119_01_T1.tar.gz"))
    'LE07_L1GT_104078_20131209_20161119_01_T1'
    >>> _dataset_name(Path("example/LE07_L1GT_104078_20131209_20161119_01_T1.tar"))
    'LE07_L1GT_104078_20131209_20161119_01_T1'
    >>> _dataset_name(Path("example/LE07_L1GT_104078_20131209_20161119_01_T2"))
    'LE07_L1GT_104078_20131209_20161119_01_T2'
    """
    # This is a little simpler than before :)
    return ds_path.stem.split(".")[0]


def _dataset_region_code(ds_path: Path) -> str:
    """
    >>> _dataset_region_code(Path("example/LE07_L1GT_104078_20131209_20161119_01_T1.tar.gz"))
    '104078'
    >>> _dataset_region_code(Path("example/LE07_L1GT_104078_20131209_20161119_01_T1.tar"))
    '104078'
    >>> _dataset_region_code(Path("example/LE07_L1GT_104078_20131209_20161119_01_T2"))
    '104078'
    """
    return _dataset_name(ds_path).split("_")[2]


if __name__ == "__main__":
    main()
