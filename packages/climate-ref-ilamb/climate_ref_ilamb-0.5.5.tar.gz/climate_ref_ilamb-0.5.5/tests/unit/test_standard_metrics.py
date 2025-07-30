import ilamb3
import pytest
from climate_ref_ilamb.standard import ILAMBStandard, _set_ilamb3_options

from climate_ref_core.dataset_registry import dataset_registry_manager
from climate_ref_core.datasets import DatasetCollection


def test_standard_site(cmip6_data_catalog, definition_factory):
    diagnostic = ILAMBStandard(
        registry_file="ilamb-test", metric_name="test-site-tas", sources={"tas": "ilamb/test/Site/tas.nc"}
    )
    ds = (
        cmip6_data_catalog[
            (cmip6_data_catalog["experiment_id"] == "historical")
            & (cmip6_data_catalog["variable_id"] == "tas")
        ]
        .groupby("instance_id")
        .first()
    )

    definition = definition_factory(
        diagnostic=diagnostic,
        cmip6=DatasetCollection(ds, "instance_id", selector=(("experiment_id", "historical"),)),
    )
    definition.output_directory.mkdir(parents=True, exist_ok=True)

    result = diagnostic.run(definition)

    assert str(result.output_bundle_filename) == "output.json"

    output_bundle_path = definition.output_directory / result.output_bundle_filename

    assert result.successful
    assert output_bundle_path.exists()
    assert output_bundle_path.is_file()

    assert str(result.metric_bundle_filename) == "diagnostic.json"

    metric_bundle_path = definition.output_directory / result.metric_bundle_filename

    assert result.successful
    assert metric_bundle_path.exists()
    assert metric_bundle_path.is_file()


def test_standard_grid(cmip6_data_catalog, definition_factory):
    diagnostic = ILAMBStandard(
        registry_file="ilamb-test",
        metric_name="test-grid-gpp",
        sources={"gpp": "ilamb/test/Grid/gpp.nc"},
        relationships={"pr": "ilamb/test/Grid/pr.nc"},
    )
    grp = cmip6_data_catalog[
        (cmip6_data_catalog["experiment_id"] == "historical")
        & ((cmip6_data_catalog["variable_id"] == "gpp") | (cmip6_data_catalog["variable_id"] == "pr"))
    ].groupby(["source_id", "member_id", "grid_label"])
    _, ds = next(iter(grp))

    definition = definition_factory(
        diagnostic=diagnostic,
        cmip6=DatasetCollection(ds, "instance_id", selector=(("experiment_id", "historical"),)),
    )
    definition.output_directory.mkdir(parents=True, exist_ok=True)

    result = diagnostic.run(definition)

    assert str(result.output_bundle_filename) == "output.json"

    output_bundle_path = definition.output_directory / result.output_bundle_filename

    assert result.successful
    assert output_bundle_path.exists()
    assert output_bundle_path.is_file()

    assert str(result.metric_bundle_filename) == "diagnostic.json"

    metric_bundle_path = definition.output_directory / result.metric_bundle_filename

    assert result.successful
    assert metric_bundle_path.exists()
    assert metric_bundle_path.is_file()


def test_standard_fail():
    with pytest.raises(ValueError):
        ILAMBStandard(
            registry_file="ilamb-test",
            metric_name="test-fail",
            sources={"gpp": "ilamb/test/Grid/gpp.nc", "pr": "ilamb/test/Grid/pr.nc"},
        )


def test_options():
    _set_ilamb3_options(dataset_registry_manager["ilamb"], "ilamb")
    assert set(["global", "tropical"]).issubset(ilamb3.conf["regions"])
