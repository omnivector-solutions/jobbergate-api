"""
Tests of the job_scripts view
"""
import json
from textwrap import dedent

import pytest

from apps.job_scripts.views import extract_sbatch_params, inject_sbatch_params


@pytest.fixture
def job_script_data_as_string():
    """
    Example of a default application script
    """
    content = json.dumps(
        {
            "application.sh": dedent(
                """\
                            #!/bin/bash

                            #SBATCH --job-name=rats
                            #SBATCH --partition=debug
                            #SBATCH --output=sample-%j.out


                            echo $SLURM_TASKS_PER_NODE
                            echo $SLURM_SUBMIT_DIR"""
            )
        }
    )
    return content


@pytest.fixture
def new_job_script_data_as_string():
    """
    Example of an application script after the injection of the sbatch params
    """
    content = json.dumps(
        {
            "application.sh": dedent(
                """\
                            #!/bin/bash

                            #SBATCH --comment=some_comment
                            #SBATCH --nice=-1
                            #SBATCH -N 10
                            #SBATCH --job-name=rats
                            #SBATCH --partition=debug
                            #SBATCH --output=sample-%j.out


                            echo $SLURM_TASKS_PER_NODE
                            echo $SLURM_SUBMIT_DIR"""
            )
        }
    )
    return content


@pytest.fixture
def sbatch_params():
    """
    String content of the argument --sbatch-params
    """
    return ("--comment=some_comment", "--nice=-1", "-N 10")


def test_inject_sbatch_params(job_script_data_as_string, sbatch_params, new_job_script_data_as_string):
    """
    Test the injection of sbatch params in a default application script
    """
    injected_string = inject_sbatch_params(job_script_data_as_string, sbatch_params)
    assert injected_string == new_job_script_data_as_string


def test_extract_sbatch_params():
    """
    Test the extraction of the params from a dict
    """
    data = {"sbatch_params_0": "foo", "sbatch_params_1": "bar", "sbatch_params_len": "2"}
    params = extract_sbatch_params(data)

    assert len(params) == 2
    assert params[0] == "foo"
    assert params[1] == "bar"


def test_extract_sbatch_params_empty():
    """
    Test the extraction of the params from a dict without params
    """
    data = {"foo": "bar"}
    params = extract_sbatch_params(data)

    assert params is None
