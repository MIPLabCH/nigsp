# -*- coding: utf-8 -*-
"""Parser for crispy-octo-broccoli."""

import argparse

from nigsp import __version__


def _get_parser():
    """
    Parse command line inputs for this function.

    Returns
    -------
    parser.parse_args() : argparse dict

    """
    parser = argparse.ArgumentParser(
        description=(
            "NiGSP, a tool to apply "
            "Graph Signal Processing to "
            "MRI (functional and structural), "
            "and compute derivative metrics "
            "such as the Structural Decoupling "
            "Index and the coupled/decoupled FC.\n"
            f"Version {__version__}"
        ),
        add_help=False,
    )
    required = parser.add_argument_group("Required Arguments")
    required.add_argument(
        "-f",
        "--input-func",
        dest="fname",
        type=str,
        help=(
            "Complete path (absolute or relative) and name "
            "of the file containing fMRI signal. This file "
            "can be a nifti, 1D, txt, csv, or mat file. "
            "If a nifti file is selected, an atlas has to "
            "be specified."
        ),
        required=True,
    )
    required.add_argument(
        "-s",
        "--input-structural",
        dest="scname",
        type=str,
        help=(
            "Complete path (absolute or relative) and name "
            "of the file containing the structural "
            "connectivity matrix. This file "
            "can be a 1D, txt, csv, or mat file."
        ),
        required=True,
    )

    opt_metrics = parser.add_argument_group(
        "Optional Arguments for metrics computation",
        description=(
            "Use these flag to "
            "select which metric "
            "should be computed. "
            "Note that the default "
            "behaviour is to compute "
            "all metrics."
        ),
    )
    opt_metrics.add_argument(
        "-sdi",
        "--structural-decoupling-index",
        dest="comp_metric",
        action="append_const",
        const="sdi",
        help=(
            "Compute the structural decoupling index "
            "(see Preti et al, 2019, Nat. Commun.)"
        ),
        default=None,
    )
    opt_metrics.add_argument(
        "-dfc",
        "--decoupled-functional-connectivity",
        dest="comp_metric",
        action="append_const",
        const="dfc",
        help=(
            "Compute the decoupledd functional connectivity "
            "(see Griffa et al, 2022, NeuroImage)"
        ),
        default=None,
    )

    opt_proc = parser.add_argument_group("Optional Arguments for data processing")
    opt_proc.add_argument(
        "-a",
        "--input-atlas",
        dest="atlasname",
        type=str,
        help=(
            "Complete path (absolute or relative) and name "
            "of the file containing the desired atlas. This "
            "file MUST be a nifti file, and it is required "
            "if the functional input is a nifti file. "
            "It is also required if the desired output is "
            "nifti. Default is None."
        ),
        default=None,
    )
    opt_proc.add_argument(
        "-idx",
        "--split-index",
        dest="index",
        type=str,
        help=(
            "The index of the harmonic that should split the "
            "harmonics in two, or the method to estimate such "
            'index. Default is "median", that invokes the '
            "estimation of the split index based on the energy "
            "of the graph."
        ),
        default="median",
    )

    opt_out = parser.add_argument_group("Optional Arguments for output")
    opt_out.add_argument(
        "-odir",
        "--output-directory",
        dest="outdir",
        type=str,
        help=(
            "Complete path (absolute or relative) and name "
            "of the desired output directory. If it does not "
            "exist, it will be created. If it is not "
            'specified, a folder named "%(prog)s" '
            "will be created in the folder containing the "
            "functional file."
        ),
        default=None,
    )
    opt_out.add_argument(
        "-ofile",
        "--output-file",
        dest="outname",
        type=str,
        help=(
            "Name of, and if desired path to, the output files."
            "Use this option to specify the file format of "
            "%(prog)s, and "
        ),
        default=None,
    )

    opt_stat = parser.add_argument_group("Optional Arguments for statistical test")

    opt_surr_type = opt_stat.add_mutually_exclusive_group()
    opt_surr_type.add_argument(
        "-sci",
        "--informed-surrogates",
        dest="surr_type",
        action="store_const",
        const="informed",
        help=(
            "Create surrogates informed of the structural "
            "connectivity matrix. Unless this option or "
            "the next one is selected, statistical test "
            "will be skipped"
        ),
        default=None,
    )
    opt_surr_type.add_argument(
        "-scu",
        "--uninformed-surrogates",
        dest="surr_type",
        action="store_const",
        const="uninformed",
        help=(
            "Create surrogates ignoring the structural "
            "connectivity matrix. Unless this option or "
            "the previous one is selected, statistical test "
            "will be skipped"
        ),
        default=None,
    )
    opt_stat.add_argument(
        "-n",
        "--surrogates-number",
        dest="n_surr",
        type=int,
        help=("Number of surrogates to create. Default is 1000."),
        default=1000,
    )
    opt_stat.add_argument(
        "-seed",
        "--random-seed",
        dest="seed",
        type=int,
        help=(
            "The seed to initialise. If None, internal "
            "seeds will be used depending on workflow, "
            "granting replicability. Default is None."
        ),
        default=None,
    )
    opt_stat.add_argument(
        "-method",
        "--statistical-method",
        dest="method",
        type=str,
        help=(
            "Type of statistical test to adopt. Possible "
            'options are "Bernoulli" (for a Bernoulli process '
            'test, group level only) or "frequentist" (for a '
            "frequentist approach, both group and subject level). "
            "Default is Bernoulli."
        ),
        default="Bernoulli",
    )

    optional = parser.add_argument_group("Other Optional Arguments")

    opt_logl = optional.add_mutually_exclusive_group()
    opt_logl.add_argument(
        "-debug",
        "--debug",
        dest="lgr_degree",
        action="store_const",
        const="debug",
        help="Only print debugging info to log file.",
        default="info",
    )
    opt_logl.add_argument(
        "-quiet",
        "--quiet",
        dest="lgr_degree",
        action="store_const",
        const="quiet",
        help="Only print warnings to log file.",
        default="info",
    )
    optional.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    optional.add_argument(
        "-v", "--version", action="version", version=("%(prog)s " + __version__)
    )
    return parser


if __name__ == "__main__":
    raise RuntimeError(
        "nigsp/cli/run.py should not be run directly;\n"
        "Please `pip install` nigsp and use the "
        "`nigsp` command"
    )


"""
Copyright 2021, Stefano Moia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
