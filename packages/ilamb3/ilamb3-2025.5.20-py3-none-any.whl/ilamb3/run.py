"""Functions for rendering ilamb3 output."""

import importlib
import re
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pooch
import xarray as xr
import yaml
from jinja2 import Template
from loguru import logger

import ilamb3
import ilamb3.analysis as anl
import ilamb3.compare as cmp
import ilamb3.dataset as dset
import ilamb3.regions as ilr
from ilamb3.analysis.base import ILAMBAnalysis, add_overall_score
from ilamb3.exceptions import AnalysisNotAppropriate
from ilamb3.transform import ALL_TRANSFORMS


def fix_pint_units(ds: xr.Dataset) -> xr.Dataset:
    def _fix(units: str) -> str:
        """
        Modify units that pint cannot handle.
        """
        try:
            val_units = float(units)
        except ValueError:
            return units
        if np.allclose(val_units, 1):
            return "dimensionless"
        if np.allclose(val_units, 1e-3):
            return "psu"
        return units

    for var, da in ds.items():
        if "units" not in da.attrs:
            continue
        ds[var].attrs["units"] = _fix(da.attrs["units"])
    return ds


def _load_reference_data(
    reference_data: pd.DataFrame,
    variable_id: str,
    sources: dict[str, str],
    relationships: dict[str, str] | None = None,
    transforms: list | None = None,
) -> xr.Dataset:
    """
    Load the reference data into containers and merge if more than 1 variable is
    used.
    """
    # First load all variables defined as `sources` or in `relationships`.
    if relationships is not None:
        sources = sources | relationships
    ref = {
        key: xr.open_dataset(reference_data.loc[str(filename), "path"])
        for key, filename in sources.items()
    }
    # Sometimes there is a bounds variable but it isn't in the attributes
    ref = {key: dset.fix_missing_bounds_attrs(ds) for key, ds in ref.items()}
    # Merge all the data together
    if len(ref) > 1:
        ref = cmp.trim_time(**ref)
        ref = cmp.same_spatial_grid(ref[variable_id], **ref)
        ds_ref = xr.merge([v for _, v in ref.items()], compat="override")
    else:
        ds_ref = ref[variable_id]
    # pint can't handle some units like `0.001`, so we have to intercept and fix
    ds_ref = fix_pint_units(ds_ref)
    # Finally apply transforms
    if transforms is not None:
        ds_ref = run_transforms(ds_ref, transforms)
    return ds_ref


def _load_comparison_data(
    df: pd.DataFrame,
    variable_id: str,
    alternate_vars: list[str] | None = None,
    related_vars: list[str] | None = None,
    transforms: list | None = None,
) -> xr.Dataset:
    """
    Load the comparison (model) data into containers and merge if more than 1
    variable is used.

    Parameters
    ----------
    df: pd.DataFrame
        The database of all possible variables and where to load them.
    variable_id: str
        The name of the variable that is the focus in the comparison.
    alternate_vars: list[str], optional
        A list of acceptable synonyms to be used if `variable_id` is not found.
    related_vars: list[str], optional
        A list of variables that can be used by transforms to product `variable_id`.
    transforms: list, optional
        A list of functions that operate on the combined dataset.
    """
    # First load all variables passed into the input dataframe. This will
    # include all relationship variables as well as alternates.
    com = {
        var: xr.open_mfdataset(sorted((df[df["variable_id"] == var]["path"]).to_list()))
        for var in df["variable_id"].unique()
    }
    # If the variable_id is not present, it may be called something else
    if alternate_vars is not None and variable_id not in com:
        found = [v for v in alternate_vars if v in com]
        if found:
            found = found[0]
            com[variable_id] = (
                com[found].rename_vars({found: variable_id})
                if found in com[found]
                else com[found]
            )
            com.pop(found)
    # If the variable_id still isn't present, we may have to apply transforms to
    # form it. Thus we load all related variables.
    if related_vars is not None and variable_id not in com:
        com = com | {
            var: xr.open_mfdataset(
                sorted((df[df["variable_id"] == var]["path"]).to_list())
            )
            for var in related_vars
            if var in df["variable_id"].unique()
        }
    # Fix bounds attributes (there is a bounds variable but it isn't in the
    # attributes)
    com = {var: dset.fix_missing_bounds_attrs(ds) for var, ds in com.items()}
    # Merge all the data together
    if len(com) > 1:
        # The grids should be the same, but sometimes models generate output
        # with very small differences in lat/lon
        try:
            com = cmp.same_spatial_grid(com[next(iter(com))], **com)
        except KeyError:
            pass
        ds_com = xr.merge([v for _, v in com.items()], compat="override")
    else:
        ds_com = com[next(iter(com))]
    # pint can't handle some units like `0.001`, so we have to intercept and fix
    ds_com = fix_pint_units(ds_com)
    # Finally apply transforms. These may create the needed variable.
    if transforms is not None:
        ds_com = run_transforms(ds_com, transforms)
    return ds_com


def registry_to_dataframe(registry: pooch.Pooch) -> pd.DataFrame:
    """
    Convert a ILAMB/IOMB registry to a DatasetCollection for use in REF.

    Parameters
    ----------
    registry : pooch.Pooch
        The pooch registry.

    Returns
    -------
    DatasetCollection
        The converted collection.
    """
    df = pd.DataFrame(
        [
            {
                "key": key,
                "path": registry.abspath / Path(key),
            }
            for key in registry.registry.keys()
        ]
    )
    return df.set_index("key")


def remove_irrelevant_variables(df: pd.DataFrame, **setup: Any) -> pd.DataFrame:
    """
    Remove unused variables from the dataframe.
    """
    reduce = df[
        df["variable_id"].isin(
            list(setup["sources"].keys())
            + list(setup.get("relationships", {}).keys())
            + setup.get("alternate_vars", [])
            + setup.get("related_vars", [])
        )
    ]
    return reduce


def run_transforms(ds: xr.Dataset, transforms: list) -> xr.Dataset:
    for transform in transforms:
        if isinstance(transform, dict):
            fcn = next(iter(transform))
            ds = ALL_TRANSFORMS[fcn](ds, **transform[fcn])
        else:
            ds = ALL_TRANSFORMS[transform](ds)
    return ds


def _load_local_assets(
    csv_file: Path, ref_file: Path, com_file: Path
) -> tuple[pd.DataFrame, xr.Dataset, xr.Dataset]:
    if not (csv_file.is_file() and ref_file.is_file() and com_file.is_file()):
        raise ValueError()
    df = pd.read_csv(str(csv_file))
    df["region"] = df["region"].astype(str).str.replace("nan", "None")
    ds_ref = xr.open_dataset(str(ref_file))
    ds_com = xr.open_dataset(str(com_file))
    return df, ds_ref, ds_com


def run_simple(
    reference_data: pd.DataFrame,
    analysis_name: str,
    comparison_data: pd.DataFrame,
    output_path: Path,
    **setup: Any,
):
    """
    Run the ILAMB standard analysis.
    """
    if "relationships" not in setup:
        setup["relationships"] = {}
    variable, analyses = setup_analyses(reference_data, **setup)

    # Thin out the dataframe to only contain possible variables we are using
    comparison_data = remove_irrelevant_variables(comparison_data, **setup)

    # Phase I: loop over each model in the group and run an analysis function
    df_all = []
    ds_com = {}
    ds_ref = None
    for _, grp in comparison_data.groupby(ilamb3.conf["comparison_groupby"]):
        row = grp.iloc[0]

        # Define what we will call the output artifacts
        source_name = "-".join([row[f] for f in ilamb3.conf["model_name_facets"]])
        csv_file = output_path / f"{source_name}.csv"
        ref_file = output_path / "Reference.nc"
        com_file = output_path / f"{source_name}.nc"
        log_file = output_path / f"{source_name}.log"
        log_id = logger.add(log_file, backtrace=True, diagnose=True)

        # Attempt to load local assets if preferred
        if ilamb3.conf["use_cached_results"]:
            try:
                dfs, ds_ref, ds_com[source_name] = _load_local_assets(
                    csv_file, ref_file, com_file
                )
                df_all.append(dfs)
                logger.info(f"Using cached information {com_file}")
                continue
            except Exception:
                pass

        try:
            # Load data and run comparison
            ref = _load_reference_data(
                reference_data,
                variable,
                setup["sources"],
                setup["relationships"],
                transforms=setup.get("transform", None),
            )
            com = _load_comparison_data(
                grp,
                variable,
                alternate_vars=setup.get("alternate_vars", []),
                related_vars=setup.get("related_vars", None),
                transforms=setup.get("transform", None),
            )
            dfs, ds_ref, ds_com[source_name] = run_analyses(ref, com, analyses)
            dfs["source"] = dfs["source"].str.replace("Comparison", source_name)

            # Write out artifacts
            dfs.to_csv(csv_file, index=False)
            if not ref_file.is_file():  # pragma: no cover
                ds_ref.to_netcdf(ref_file)
            ds_com[source_name].to_netcdf(com_file)
            df_all.append(dfs)
        except Exception:  # pragma: no cover
            logger.exception(
                f"ILAMB analysis '{analysis_name}' failed for '{source_name}'."
            )
            continue

        # Pop log and remove zero size files
        logger.remove(log_id)
        if log_file.stat().st_size == 0:  # pragma: no cover
            log_file.unlink()

    # Check that the reference intermediate data really was generated.
    if ds_ref is None:
        raise ValueError(
            "Reference intermediate data was not generated."
        )  # pragma: no cover

    # Phase 2: get plots and combine scalars and save
    plt.rcParams.update({"figure.max_open_warning": 0})
    df = pd.concat(df_all).drop_duplicates(
        subset=["source", "region", "analysis", "name"]
    )
    df = add_overall_score(df)
    df_plots = plot_analyses(df, ds_ref, ds_com, analyses, output_path)

    # Generate an output page
    if ilamb3.conf["debug_mode"] and (output_path / "index.html").is_file():
        return
    ds_ref.attrs["header"] = analysis_name
    html = generate_html_page(df, ds_ref, ds_com, df_plots)
    with open(output_path / "index.html", mode="w") as out:
        out.write(html)


def setup_analyses(
    reference_data: pd.DataFrame, **analysis_setup: Any
) -> tuple[str, dict[str, ILAMBAnalysis]]:
    """.

    sources
    relationships

    variable_cmap
    skip_XXX

    """
    # Make sure we can index the reference data
    if reference_data.index.name != "key":
        reference_data = reference_data.set_index("key")

    # Check on sources
    sources = analysis_setup.get("sources", {})
    relationships = analysis_setup.get("relationships", {})
    if len(sources) != 1:
        raise ValueError(
            f"The default ILAMB analysis requires a single variable and source, but I found: {sources}"
        )
    variable = list(sources.keys())[0]

    # Augment options with things in the global options
    if "regions" not in analysis_setup:
        analysis_setup["regions"] = ilamb3.conf["regions"]
    if "method" not in analysis_setup:
        if ilamb3.conf["prefer_regional_quantiles"]:
            analysis_setup["method"] = "RegionalQuantiles"
            analysis_setup["quantile_database"] = pd.read_parquet(
                reference_data.loc[ilamb3.conf["quantile_database"], "path"]
            )
            analysis_setup["quantile_threshold"] = ilamb3.conf["quantile_threshold"]
            ilr.Regions().add_netcdf(
                xr.load_dataset(reference_data.loc["regions/Whittaker.nc", "path"])
            )
        else:
            analysis_setup["method"] = "Collier2018"
    if "use_uncertainty" not in analysis_setup:
        analysis_setup["use_uncertainty"] = ilamb3.conf["use_uncertainty"]

    # If specialized analyses are given, setup those and return
    if "analyses" in analysis_setup:
        analysis_setup["required_variable"] = variable
        analyses = {
            a: anl.ALL_ANALYSES[a](**analysis_setup)
            for a in analysis_setup.pop("analyses", [])
            if a in anl.ALL_ANALYSES
        }
        return variable, analyses

    # Setup the default analysis
    analyses = {
        name: a(variable, **analysis_setup)
        for name, a in anl.DEFAULT_ANALYSES.items()
        if analysis_setup.get(f"skip_{name.lower()}", False) is False
    }
    analyses.update(
        {
            f"Relationship {ind_variable}": anl.relationship_analysis(
                variable, ind_variable, **analysis_setup
            )
            for ind_variable in relationships
        }
    )
    return variable, analyses


def run_analyses(
    ref: xr.Dataset, com: xr.Dataset, analyses: dict[str, ILAMBAnalysis]
) -> tuple[pd.DataFrame, xr.Dataset, xr.Dataset]:
    """
    Run the input analyses on the given reference and comparison datasets.

    Parameters
    ----------
    ref : xr.Dataset
        The dataset which will be considered as the reference.
    com : xr.Dataset
        The dataset which will be considered as the comparison.
    analyses: dict[str, ILAMBAnalysis]
        A dictionary of analyses to

    Returns
    -------
    pd.DataFrame, xr.Dataset, xr.Dataset
        Analysis output, dataframe with scalar information and datasets with
        reference and comparison information for plotting.
    """
    dfs = []
    ds_refs = []
    ds_coms = []
    for aname, a in analyses.items():
        try:
            df, ds_ref, ds_com = a(ref, com)
        except AnalysisNotAppropriate:
            continue
        dfs.append(df)
        ds_refs.append(ds_ref)
        ds_coms.append(ds_com)
    dfs = pd.concat(dfs, ignore_index=True)
    dfs["name"] = dfs["name"] + " [" + dfs["units"] + "]"
    ds_ref = xr.merge(ds_refs)
    ds_com = xr.merge(ds_coms)
    return dfs, ds_ref, ds_com


def regenerate_figs(path: Path) -> bool:
    """
    Do we need to regenerate the figures?
    """
    path.mkdir(exist_ok=True, parents=True)
    png_files = list(path.glob("*.png"))
    if not png_files:
        return True
    first_png_time = min([p.stat().st_mtime for p in png_files])
    nc_files = list(path.glob("*.nc"))
    if not nc_files:
        return True
    last_nc_time = max([p.stat().st_mtime for p in nc_files])
    if last_nc_time > first_png_time:
        return True
    return False


def plot_analyses(
    df: pd.DataFrame,
    ref: xr.Dataset,
    com: dict[str, xr.Dataset],
    analyses: dict[str, ILAMBAnalysis],
    plot_path: Path,
) -> pd.DataFrame:
    """
    Plot analysis output encoded in each analysis.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of all scalars from the analyses.
    ref : xr.Dataset
        A dataset containing reference data for plotting.
    com : dict[str,xr.Dataset]
        A dictionary of the comparison datasets whose keys are the model names.
    analyses : dict[str, ILAMBAnalysis]
        A dictionary of analyses to
    plot_path : Path
        A path to prepend all filenames.

    Returns
    -------
    pd.DataFrame
        A dataframe containing plot information and matplotlib axes.
    """
    if ilamb3.conf["debug_mode"] and not regenerate_figs(plot_path):
        return pd.DataFrame([])
    plot_path.mkdir(exist_ok=True, parents=True)
    df_plots = []
    for name, a in analyses.items():
        dfp = a.plots(df, ref, com)
        for _, row in dfp.iterrows():
            row["axis"].get_figure().savefig(
                plot_path / f"{row['source']}_{row['region']}_{row['name']}.png"
            )
        plt.close("all")
        if "analysis" not in dfp.columns:
            dfp["analysis"] = name
        df_plots.append(dfp)
    df_plots = pd.concat(df_plots)
    return df_plots


def generate_html_page(
    df: pd.DataFrame,
    ref: xr.Dataset,
    com: dict[str, xr.Dataset],
    df_plots: pd.DataFrame,
) -> str:
    """
    Generate an html page encoding all analysis data.

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe of all scalars from the analyses.
    ref : xr.Dataset
        A dataset containing reference data for plotting.
    com : dict[str,xr.Dataset]
        A dictionary of the comparison datasets whose keys are the model names.
    df_plots : pd.DataFrame
        A dataframe containing plot information and matplotlib axes.

    Returns
    -------
    str
        The html page.
    """
    ilamb_regions = ilr.Regions()
    # Setup template analyses and plots
    analyses = {analysis: {} for analysis in df["analysis"].dropna().unique()}
    for (aname, pname), df_grp in df_plots.groupby(["analysis", "name"], sort=False):
        analyses[aname][pname] = []
        if len(df_grp["source"].unique()) == 1 and None in df_grp["source"].unique():
            analyses[aname][pname] += [{"None": f"None_RNAME_{pname}.png"}]
            continue
        if "Reference" in df_grp["source"].unique():
            analyses[aname][pname] += [{"Reference": f"Reference_RNAME_{pname}.png"}]
        analyses[aname][pname] += [{"Model": f"MNAME_RNAME_{pname}.png"}]
    ref_plots = list(df_plots[df_plots["source"] == "Reference"]["name"].unique())
    mod_plots = list(
        df_plots[~df_plots["source"].isin(["Reference", None])]["name"].unique()
    )
    all_plots = sorted(list(set(ref_plots) | set(mod_plots)))
    if not all_plots:
        all_plots = [""]

    # Setup template dictionary
    df = df.reset_index(drop=True)
    df["id"] = df.index
    data = {
        "page_header": ref.attrs["header"] if "header" in ref.attrs else "",
        "analysis_list": list(analyses.keys()),
        "model_names": [m for m in df["source"].unique() if m != "Reference"],
        "ref_plots": ref_plots,
        "mod_plots": mod_plots,
        "all_plots": all_plots,
        "regions": {
            (None if key == "None" else key): (
                "All Data" if key == "None" else ilamb_regions.get_name(key)
            )
            for key in df["region"].unique()
        },
        "analyses": analyses,
        "data_information": {
            key.capitalize(): ref.attrs[key]
            for key in ["title", "institution", "version", "doi"]
            if key in ref.attrs
        },
        "table_data": str(
            [row.to_dict() for _, row in df.drop(columns="units").iterrows()]
        ).replace("nan", "NaN"),
    }

    # Generate the html from the template
    template = importlib.resources.open_text(
        "ilamb3.templates", "dataset_page.html"
    ).read()
    html = Template(template).render(data)
    return html


def _flatten_dict(d: dict, parent_key: str = "", sep: str = "/") -> dict:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict) and "sources" not in v:
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def _clean_pathname(filename: str) -> str:
    """Removes characters we do not want in our paths."""
    invalid_chars = r'[\\/:*?"<>|\s]'
    cleaned_filename = re.sub(invalid_chars, "", filename)
    return cleaned_filename


def _is_leaf(current: dict) -> bool:
    """Is the current item in the nested dictionary a leaf?"""
    if not isinstance(current, dict):
        return False
    if "sources" in current:
        return True
    return False


def _add_path(current: dict, path: Path | None = None) -> dict:
    """Recursively add the nested dictionary headings as a `path` in the leaves."""
    path = Path() if path is None else path
    for key, val in current.items():
        if not isinstance(val, dict):
            continue
        key_path = path / Path(_clean_pathname(key))
        if _is_leaf(val):
            val["path"] = str(key_path)
        else:
            current[key] = _add_path(val, key_path)
    return current


def _to_leaf_list(current: dict, leaf_list: list | None = None) -> list:
    """Recursively flatten the nested dictionary only returning the leaves."""
    leaf_list = [] if leaf_list is None else leaf_list
    for _, val in current.items():
        if not isinstance(val, dict):
            continue
        if _is_leaf(val):
            leaf_list.append(val)
        else:
            _to_leaf_list(val, leaf_list)
    return leaf_list


def _create_paths(current: dict, root: Path):
    """Recursively ensure paths in the leaves are created."""
    for _, val in current.items():
        if not isinstance(val, dict):
            continue
        if _is_leaf(val):
            if "path" in val:
                (root / Path(val["path"])).mkdir(parents=True, exist_ok=True)
        else:
            _create_paths(val, root)


def parse_benchmark_setup(yaml_file: str | Path) -> dict:
    """Parse the file which is analagous to the old configure file."""
    yaml_file = Path(yaml_file)
    with open(yaml_file) as fin:
        analyses = yaml.safe_load(fin)
    assert isinstance(analyses, dict)
    return analyses


def run_study(
    study_setup: str,
    df_datasets: pd.DataFrame,
    ref_datasets: pd.DataFrame | None = None,
    output_path: str | Path = "_build",
):
    output_path = Path(output_path)
    # Some yaml text that would get parsed like a dictionary.
    analyses = parse_benchmark_setup(study_setup)
    registry = analyses.pop("registry") if "registry" in analyses else "ilamb.txt"
    if registry == "ilamb.txt":
        reg = ilamb3.ilamb_catalog()
    elif registry == "iomb.txt":
        reg = ilamb3.iomb_catalog()
    else:
        raise ValueError("Unsupported registry.")

    # The yaml analysis setup can be as structured as the user needs. We are no longer
    # limited to the `h1` and `h2` headers from ILAMB 2.x. We will detect leaf nodes by
    # the presence of a `sources` dictionary.
    analyses = _add_path(analyses)

    # Various traversal actions
    _create_paths(analyses, output_path)

    # Create a list of just the leaves to use in creation all work combinations
    analyses_list = _to_leaf_list(analyses)

    # Run the confrontations
    for analysis in analyses_list:
        path = analysis.pop("path")
        try:
            run_simple(
                (
                    ref_datasets
                    if ref_datasets is not None
                    else registry_to_dataframe(reg)
                ),
                path.split("/")[-1],
                df_datasets,
                output_path / path,
                **analysis,
            )
        except Exception:
            continue
