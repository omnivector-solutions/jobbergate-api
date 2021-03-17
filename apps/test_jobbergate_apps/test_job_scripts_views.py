import pytest

from apps.job_scripts.views import inject_sbatch_params


@pytest.fixture
def job_script_data_as_string():
    content = '{"application.sh": "#!/bin/bash\\n\\n#SBATCH --job-name=rats\\n#SBATCH --partition=debug\\n#SBATCH --output=sample-%j.out\\n\\n\\necho $SLURM_TASKS_PER_NODE\\necho $SLURM_SUBMIT_DIR\\necho $SLURM_NODE_ALIASES\\necho $SLURM_CLUSTER_NAME\\necho $SLURM_JOB_CPUS_PER_NODE\\necho $SLURM_JOB_PARTITION\\necho $SLURM_JOB_NUM_NODES\\necho $SLURM_JOBID\\necho $SLURM_NODELIST\\necho $SLURM_NNODES\\necho $SLURM_SUBMIT_HOST\\necho $SLURM_JOB_ID\\necho $SLURM_CONF\\necho $SLURM_JOB_NAME\\necho$SLURM_JOB_NODELIST"}'
    return content


@pytest.fixture
def new_job_script_data_as_string():
    content = '{"application.sh": "#!/bin/bash\\n\\n#SBATCH --comment=some_comment\\n#SBATCH --nice=-1\\n#SBATCH --job-name=rats\\n#SBATCH --partition=debug\\n#SBATCH --output=sample-%j.out\\n\\n\\necho $SLURM_TASKS_PER_NODE\\necho $SLURM_SUBMIT_DIR\\necho $SLURM_NODE_ALIASES\\necho $SLURM_CLUSTER_NAME\\necho $SLURM_JOB_CPUS_PER_NODE\\necho $SLURM_JOB_PARTITION\\necho $SLURM_JOB_NUM_NODES\\necho $SLURM_JOBID\\necho $SLURM_NODELIST\\necho $SLURM_NNODES\\necho $SLURM_SUBMIT_HOST\\necho $SLURM_JOB_ID\\necho $SLURM_CONF\\necho $SLURM_JOB_NAME\\necho$SLURM_JOB_NODELIST"}'
    return content


@pytest.fixture
def sbatch_params():
    return "--comment=some_comment --nice=-1"


def test_inject_sbatch_params(job_script_data_as_string, sbatch_params, new_job_script_data_as_string):
    injected_string = inject_sbatch_params(job_script_data_as_string, sbatch_params)
    assert injected_string == new_job_script_data_as_string
