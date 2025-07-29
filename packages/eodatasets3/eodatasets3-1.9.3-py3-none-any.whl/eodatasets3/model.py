from pathlib import Path
from uuid import UUID

import affine
import attr
from ruamel.yaml.comments import CommentedMap
from shapely.geometry.base import BaseGeometry

from eodatasets3.properties import Eo3Dict, Eo3Interface

DEA_URI_PREFIX = "https://collections.dea.ga.gov.au"
ODC_DATASET_SCHEMA_URL = "https://schemas.opendatacube.org/dataset"

# Either a local filesystem path or a string URI.
# (the URI can use any scheme supported by rasterio, such as tar:// or https:// or ...)
Location = Path | str


@attr.s(auto_attribs=True, slots=True)
class ProductDoc:
    """
    The product that this dataset belongs to.

    "name" is the local name in ODC.

    href is intended as a more global unique "identifier" uri for the product.
    """

    name: str | None = None
    href: str | None = None


@attr.s(auto_attribs=True, slots=True, hash=True)
class GridDoc:
    """The grid describing a measurement/band's pixels"""

    shape: tuple[int, int]
    transform: affine.Affine


@attr.s(auto_attribs=True, slots=True)
class MeasurementDoc:
    """
    A Dataset's reference to a measurement file.
    """

    path: str
    band: int | None = 1
    layer: str | None = None
    grid: str = "default"

    name: str = attr.ib(metadata=dict(doc_exclude=True), default=None)
    alias: str = attr.ib(metadata=dict(doc_exclude=True), default=None)


@attr.s(auto_attribs=True, slots=True)
class AccessoryDoc:
    """
    An accessory is an extra file included in the dataset that is not
    a measurement/band.

    For example: thumbnails, alternative metadata documents, or checksum files.
    """

    path: str
    type: str | None = None
    name: str = attr.ib(metadata=dict(doc_exclude=True), default=None)


@attr.s(auto_attribs=True, slots=True)
class DatasetDoc(Eo3Interface):
    """
    An EO3 dataset document

    Includes :class:`.Eo3Interface` methods for metadata access::

        >>> p = DatasetDoc()
        >>> p.platform = 'LANDSAT_8'
        >>> p.processed = '2018-04-03'
        >>> p.properties['odc:processing_datetime']
        datetime.datetime(2018, 4, 3, 0, 0, tzinfo=datetime.timezone.utc)

    """

    #: Dataset UUID
    id: UUID | None = None
    #: Human-readable identifier for the dataset
    label: str | None = None
    #: The product name (local) and/or url (global)
    product: ProductDoc | None = None
    #: Location(s) where this dataset is stored.
    #:
    #: (ODC supports multiple locations when the same dataset is stored in multiple places)
    #:
    #: They are fully qualified URIs (``file://...`, ``https://...``, ``s3://...``)
    #:
    #: All other paths in the document (measurements, accessories) are relative to the
    #: chosen location.
    locations: list[str] | None = None

    #: CRS string. Eg. ``epsg:3577``
    crs: str | None = None
    #: Shapely geometry of the valid data coverage
    #:
    #: (it must contain all non-empty pixels of the image)
    geometry: BaseGeometry | None = None
    #: Grid specifications for measurements
    grids: dict[str, GridDoc] | None = None
    #: Raw properties
    properties: Eo3Dict = attr.ib(factory=Eo3Dict)
    #: Loadable measurements of the dataset
    measurements: dict[str, MeasurementDoc] | None = None
    #: References to accessory files
    #:
    #: Such as thumbnails, checksums, other kinds of metadata files.
    #:
    #: (any files included in the dataset that are not measurements)
    accessories: dict[str, AccessoryDoc] = attr.ib(factory=CommentedMap)
    #: Links to source dataset uuids
    lineage: dict[str, list[UUID]] = attr.ib(factory=CommentedMap)
