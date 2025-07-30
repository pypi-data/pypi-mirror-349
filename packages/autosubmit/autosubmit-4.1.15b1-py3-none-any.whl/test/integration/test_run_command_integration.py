# Copyright 2015-2025 Earth Sciences Department, BSC-CNS
#
# This file is part of Autosubmit.
#
# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import os
import pwd
import shutil
import sqlite3
from pathlib import Path

import pytest

from autosubmit.autosubmit import Autosubmit
from autosubmitconfigparser.config.configcommon import AutosubmitConfig
from test.unit.utils.common import create_database, init_expid


def _get_script_files_path() -> Path:
    return Path(__file__).resolve().parent / 'files'


# TODO expand the tests to test Slurm, PSPlatform, Ecplatform whenever possible

@pytest.fixture
def run_tmpdir(tmpdir_factory):
    folder = tmpdir_factory.mktemp('run_tests')
    os.mkdir(folder.join('scratch'))
    os.mkdir(folder.join('run_tmp_dir'))
    file_stat = os.stat(f"{folder.strpath}")
    file_owner_id = file_stat.st_uid
    file_owner = pwd.getpwuid(file_owner_id).pw_name
    folder.owner = file_owner

    # Write an autosubmitrc file in the temporary directory
    autosubmitrc = folder.join('autosubmitrc')
    autosubmitrc.write(f'''
[database]
path = {folder}
filename = tests.db

[local]
path = {folder}

[globallogs]
path = {folder}

[structures]
path = {folder}

[historicdb]
path = {folder}

[historiclog]
path = {folder}

[defaultstats]
path = {folder}

''')
    os.environ['AUTOSUBMIT_CONFIGURATION'] = str(folder.join('autosubmitrc'))
    create_database(str(folder.join('autosubmitrc')))
    assert "tests.db" in [Path(f).name for f in folder.listdir()]
    init_expid(str(folder.join('autosubmitrc')), platform='local', create=False, test_type='test')
    assert "t000" in [Path(f).name for f in folder.listdir()]
    return folder


@pytest.fixture
def prepare_run(run_tmpdir):
    # touch as_misc
    # remove files under t000/conf
    conf_folder = Path(f"{run_tmpdir.strpath}/t000/conf")
    shutil.rmtree(conf_folder)
    os.makedirs(conf_folder)
    platforms_path = Path(f"{run_tmpdir.strpath}/t000/conf/platforms.yml")
    main_path = Path(f"{run_tmpdir.strpath}/t000/conf/AAAmain.yml")
    # Add each platform to test
    with platforms_path.open('w') as f:
        f.write(f"""
PLATFORMS:
    dummy:
        type: dummy
        """)

    with main_path.open('w') as f:
        f.write("""
EXPERIMENT:
    # List of start dates
    DATELIST: '20000101'
    # List of members.
    MEMBERS: fc0
    # Unit of the chunk size. Can be hour, day, month, or year.
    CHUNKSIZEUNIT: month
    # Size of each chunk.
    CHUNKSIZE: '2'
    # Number of chunks of the experiment.
    NUMCHUNKS: '3'  
    CHUNKINI: ''
    # Calendar used for the experiment. Can be standard or noleap.
    CALENDAR: standard

CONFIG:
    # Current version of Autosubmit.
    AUTOSUBMIT_VERSION: ""
    # Total number of jobs in the workflow.
    TOTALJOBS: 3
    # Maximum number of jobs permitted in the waiting status.
    MAXWAITINGJOBS: 3
    SAFETYSLEEPTIME: 0
DEFAULT:
    # Job experiment ID.
    EXPID: "t000"
    # Default HPC platform name.
    HPCARCH: "local"
    #hint: use %PROJDIR% to point to the project folder (where the project is cloned)
    # Custom configuration location.
project:
    # Type of the project.
    PROJECT_TYPE: None
    # Folder to hold the project sources.
    PROJECT_DESTINATION: local_project
AUTOSUBMIT:
    WORKFLOW_COMMIT: "debug-commit-hash"
""")
    expid_dir = Path(f"{run_tmpdir.strpath}/scratch/whatever/{run_tmpdir.owner}/t000")
    dummy_dir = Path(f"{run_tmpdir.strpath}/scratch/whatever/{run_tmpdir.owner}/t000/dummy_dir")
    real_data = Path(f"{run_tmpdir.strpath}/scratch/whatever/{run_tmpdir.owner}/t000/real_data")
    # We write some dummy data inside the scratch_dir
    os.makedirs(expid_dir, exist_ok=True)
    os.makedirs(dummy_dir, exist_ok=True)
    os.makedirs(real_data, exist_ok=True)

    with open(dummy_dir.joinpath('dummy_file'), 'w') as f:
        f.write('dummy data')
    # create some dummy absolute symlinks in expid_dir to test migrate function
    (real_data / 'dummy_symlink').symlink_to(dummy_dir / 'dummy_file')
    return run_tmpdir


def check_db_fields(run_tmpdir,
                    expected_entries: int,
                    final_status: str,
                    wrapper_type: str) -> dict:
    """
    Validate the database state after a completed run.

    :param run_tmpdir: Temporary directory for the test run.
    :type run_tmpdir: pytest.TempPathFactory
    :param expected_entries: The expected number of entries in the database.
    :type expected_entries: int
    :param final_status: The expected final status of the jobs ("COMPLETED", "FAILED").
    :type final_status: str
    :param wrapper_type: The type of wrapper used in the test ("vertical").
    :type wrapper_type: str
    :return: A dictionary containing the results of various database checks,
             including the existence of the database, the number of entries,
             and the validity of job fields.
    :rtype: dict
    """
    db_check_list = {}
    # Test database exists.
    job_data = Path(f"{run_tmpdir.strpath}/job_data_t000.db")
    autosubmit_db = Path(f"{run_tmpdir.strpath}/tests.db")
    db_check_list["JOB_DATA_EXIST"] = job_data.exists()
    db_check_list["AUTOSUBMIT_DB_EXIST"] = autosubmit_db.exists()

    # Check job_data info
    conn = sqlite3.connect(job_data)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM job_data")
    rows = c.fetchall()
    db_check_list["JOB_DATA_ENTRIES"] = len(rows) == expected_entries
    # Convert rows to a list of dictionaries
    rows_as_dicts = [dict(row) for row in rows]
    # Tune the print so it is more readable, so it is easier to debug in case of failure
    db_check_list["JOB_DATA_FIELDS"] = {}
    counter_by_name = {}
    group_by_job_name = {
        job_name: sorted(
            [row for row in rows_as_dicts if row["job_name"] == job_name],
            key=lambda x: x["job_id"]
        )
        for job_name in {row["job_name"] for row in rows_as_dicts}
    }

    for job_name, grouped_rows in group_by_job_name.items():
        counter_by_name[job_name] = len(grouped_rows)
        if job_name not in db_check_list["JOB_DATA_FIELDS"]:
            db_check_list["JOB_DATA_FIELDS"][job_name] = {}

        previous_retry_row = {}
        for i, row_dict in enumerate(grouped_rows):
            db_check_list["JOB_DATA_FIELDS"][job_name][i] = {}
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["submit"] = \
                row_dict["submit"] > 0 and row_dict["submit"] != 1970010101
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["start"] = \
                row_dict["start"] > 0 and row_dict["start"] != 1970010101
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["finish"] = \
                row_dict["finish"] > 0 and row_dict["finish"] != 1970010101
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["start>submit"] = \
                int(row_dict["start"]) >= int(row_dict["submit"])
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["finish>start"] = \
                int(row_dict["finish"]) >= int(row_dict["start"])
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["finish>submit"] = \
                int(row_dict["finish"]) >= int(row_dict["submit"])
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["status"] = \
                row_dict["status"] == final_status
            db_check_list["JOB_DATA_FIELDS"][job_name][i]["workflow_commit"] = \
                row_dict["workflow_commit"] == "debug-commit-hash"
            # Check for empty fields
            empty_fields = []
            for key in [key for key in row_dict.keys() if
                        key not in ["status", "finish", "submit", "start", "extra_data", "children",
                                    "platform_output"]]:
                if str(row_dict[key]) == str(""):
                    empty_fields.append(key)

            if previous_retry_row:
                # check submit
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["submit>=previous_submit_retry"] = \
                    row_dict["submit"] >= previous_retry_row["submit"]
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["submit>previous_submit_retry"] = \
                    row_dict["submit"] >= previous_retry_row["finish"]
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["submit>previous_start_retry"] = \
                    row_dict["submit"] >= previous_retry_row["start"]


                # check start
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["start>=previous_start_retry"] = \
                    row_dict["start"] >= previous_retry_row["start"]
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["start>=previous_finish_retry"] = \
                    row_dict["start"] >= previous_retry_row["finish"]
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["start>=previous_submit_retry"] = \
                    row_dict["start"] >= previous_retry_row["submit"]

                # check finish
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["finish>=previous_finish_retry"] = \
                    row_dict["finish"] >= previous_retry_row["finish"]
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["finish>=previous_start_retry"] = \
                    row_dict["finish"] >= previous_retry_row["start"]
                db_check_list["JOB_DATA_FIELDS"][job_name][i]["finish>=previous_submit_retry"] = \
                    row_dict["finish"] >= previous_retry_row["submit"]

            previous_retry_row = row_dict
    print_db_results(db_check_list, rows_as_dicts, run_tmpdir)
    c.close()
    conn.close()
    return db_check_list


def print_db_results(db_check_list, rows_as_dicts, run_tmpdir):
    """
    Print the database check results.
    """
    column_names = rows_as_dicts[0].keys() if rows_as_dicts else []
    column_widths = [max(len(str(row[col])) for row in rows_as_dicts + [dict(zip(column_names, column_names))]) for col
                     in column_names]
    print(f"Experiment folder: {run_tmpdir.strpath}")
    header = " | ".join(f"{name:<{width}}" for name, width in zip(column_names, column_widths))
    print(f"\n{header}")
    print("-" * len(header))
    # Print the rows
    for row_dict in rows_as_dicts:  # always print, for debug proposes
        print(" | ".join(f"{str(row_dict[col]):<{width}}" for col, width in zip(column_names, column_widths)))
    # Print the results
    print("\nDatabase check results:")
    print(f"JOB_DATA_EXIST: {db_check_list['JOB_DATA_EXIST']}")
    print(f"AUTOSUBMIT_DB_EXIST: {db_check_list['AUTOSUBMIT_DB_EXIST']}")
    print(f"JOB_DATA_ENTRIES_ARE_CORRECT: {db_check_list['JOB_DATA_ENTRIES']}")

    for job_name in db_check_list["JOB_DATA_FIELDS"]:
        for job_counter in db_check_list["JOB_DATA_FIELDS"][job_name]:
            all_ok = True
            for field in db_check_list["JOB_DATA_FIELDS"][job_name][job_counter]:
                if field == "empty_fields":
                    if len(db_check_list['JOB_DATA_FIELDS'][job_name][job_counter][field]) > 0:
                        all_ok = False
                        print(f"{field} assert FAILED")
                else:
                    if not db_check_list['JOB_DATA_FIELDS'][job_name][job_counter][field]:
                        all_ok = False
                        print(f"{field} assert FAILED")
            if int(job_counter) > 0:
                print(f"Job entry: {job_name} retrial: {job_counter} assert {str(all_ok).upper()}")
            else:
                print(f"Job entry: {job_name} assert {str(all_ok).upper()}")


def assert_db_fields(db_check_list):
    """
    Assert that the database fields are correct.
    """
    assert db_check_list["JOB_DATA_EXIST"]
    assert db_check_list["AUTOSUBMIT_DB_EXIST"]
    assert db_check_list["JOB_DATA_ENTRIES"]
    for job_name in db_check_list["JOB_DATA_FIELDS"]:
        for job_counter in db_check_list["JOB_DATA_FIELDS"][job_name]:
            for field in db_check_list["JOB_DATA_FIELDS"][job_name][job_counter]:
                if field == "empty_fields":
                    assert len(db_check_list['JOB_DATA_FIELDS'][job_name][job_counter][field]) == 0
                else:
                    assert db_check_list['JOB_DATA_FIELDS'][job_name][job_counter][field]


def assert_exit_code(final_status, exit_code):
    """
    Check that the exit code is correct.
    """
    if final_status == "FAILED":
        assert exit_code > 0
    else:
        assert exit_code == 0


def check_files_recovered(run_tmpdir, log_dir, expected_files) -> dict:
    """
    Check that all files are recovered after a run.
    """
    # Check logs recovered and all stat files exists.
    as_conf = AutosubmitConfig("t000")
    as_conf.reload()
    retrials = as_conf.experiment_data['JOBS']['JOB'].get('RETRIALS', 0)
    files_check_list = {}
    for f in log_dir.glob('*'):
        files_check_list[f.name] = not any(
            str(f).endswith(f".{i}.err") or str(f).endswith(f".{i}.out") for i in range(retrials + 1))
    stat_files = [str(f).split("_")[-1] for f in log_dir.glob('*') if "STAT" in str(f)]
    for i in range(retrials + 1):
        files_check_list[f"STAT_{i}"] = str(i) in stat_files

    print("\nFiles check results:")
    all_ok = True
    for file in files_check_list:
        if not files_check_list[file]:
            all_ok = False
            print(f"{file} does not exists: {files_check_list[file]}")
    if all_ok:
        print("All log files downloaded are renamed correctly.")
    else:
        print("Some log files are not renamed correctly.")
    files_err_out_found = [f for f in log_dir.glob('*') if (
            str(f).endswith(".err") or str(f).endswith(".out") or "retrial" in str(
        f).lower()) and "ASThread" not in str(f)]
    files_check_list["EXPECTED_FILES"] = len(files_err_out_found) == expected_files
    if not files_check_list["EXPECTED_FILES"]:
        print(f"Expected number of log files: {expected_files}. Found: {len(files_err_out_found)}")
        files_err_out_found_str = ", ".join([f.name for f in files_err_out_found])
        print(f"Log files found: {files_err_out_found_str}")
        print("Log files content:")
        for f in files_err_out_found:
            print(f"File: {f.name}\n{f.read_text()}")
        print("All files, permissions and owner:")
        for f in log_dir.glob('*'):
            file_stat = os.stat(f)
            file_owner_id = file_stat.st_uid
            file_owner = pwd.getpwuid(file_owner_id).pw_name
            print(f"File: {f.name} owner: {file_owner} permissions: {oct(file_stat.st_mode)}")
    else:
        print(f"All log files are gathered: {expected_files}")
    return files_check_list


def assert_files_recovered(files_check_list):
    """
    Assert that the files are recovered correctly.
    """
    for check_name in files_check_list:
        assert files_check_list[check_name]


def init_run(run_tmpdir, jobs_data):
    """
    Initialize the run, writing the jobs.yml file and creating the experiment.
    """
    # write jobs_data
    jobs_path = Path(f"{run_tmpdir.strpath}/t000/conf/jobs.yml")
    log_dir = Path(f"{run_tmpdir.strpath}/t000/tmp/LOG_t000")
    with jobs_path.open('w') as f:
        f.write(jobs_data)

    # Create
    init_expid(os.environ["AUTOSUBMIT_CONFIGURATION"], platform='local', expid='t000', create=True, test_type='test')

    # This is set in _init_log which is not called
    as_misc = Path(f"{run_tmpdir.strpath}/t000/conf/as_misc.yml")
    with as_misc.open('w') as f:
        f.write("""
    AS_MISC: True
    ASMISC:
        COMMAND: run
    AS_COMMAND: run
            """)
    return log_dir


@pytest.mark.parametrize("jobs_data, expected_db_entries, final_status, wrapper_type", [
    # Success
    ("""
    EXPERIMENT:
        NUMCHUNKS: '3'
    JOBS:
        job:
            SCRIPT: |
                echo "Hello World with id=Success"
                sleep 1
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01

    """, 3, "COMPLETED", "simple"),  # No wrappers, simple type
    # Success wrapper
    ("""
    EXPERIMENT:
        NUMCHUNKS: '2'
    JOBS:
        job:
            SCRIPT: |
                echo "Hello World with id=Success + wrappers"
                sleep 1
            DEPENDENCIES: job-1
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01

        job2:
            SCRIPT: |
                echo "Hello World with id=Success + wrappers"
                sleep 1
            DEPENDENCIES: job2-1
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01

    wrappers:
        wrapper:
            JOBS_IN_WRAPPER: job
            TYPE: vertical
        wrapper2:
            JOBS_IN_WRAPPER: job2
            TYPE: vertical
    """, 4, "COMPLETED", "vertical"),  # Wrappers present, vertical type
    # Failure
    ("""
    JOBS:
        job:
            SCRIPT: |
                sleep 2
                decho "Hello World with id=FAILED"
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01
            retrials: 2  # In local, it started to fail at 18 retrials.
    """, (2 + 1) * 3, "FAILED", "simple"),  # No wrappers, simple type
    # Failure wrappers
    ("""
    JOBS:
        job:
            SCRIPT: |
                sleep 2
                decho "Hello World with id=FAILED + wrappers"
            PLATFORM: local
            DEPENDENCIES: job-1
            RUNNING: chunk
            wallclock: 00:10
            retrials: 2
    wrappers:
        wrapper:
            JOBS_IN_WRAPPER: job
            TYPE: vertical
    """, (2 + 1) * 1, "FAILED", "vertical"),  # Wrappers present, vertical type
], ids=["Success", "Success with wrapper", "Failure", "Failure with wrapper"])
def test_run_uninterrupted(run_tmpdir, prepare_run, jobs_data, expected_db_entries, final_status, wrapper_type):
    log_dir = init_run(run_tmpdir, jobs_data)
    # Run the experiment
    exit_code = Autosubmit.run_experiment(expid='t000')

    # Check and display results
    db_check_list = check_db_fields(run_tmpdir, expected_db_entries, final_status, wrapper_type)
    files_check_list = check_files_recovered(run_tmpdir, log_dir, expected_files=expected_db_entries * 2)

    e_msg = f"Current folder: {run_tmpdir.strpath}\n"
    e_msg += f"sqlitebrowser {run_tmpdir.strpath}/job_data_t000.db\n"
    for check, value in db_check_list.items():
        if not value:
            e_msg += f"{check}: {value}\n"
        elif isinstance(value, dict):
            for job_name in value:
                for job_counter in value[job_name]:
                    for check_name, value_ in value[job_name][job_counter].items():
                        if not value_:
                            e_msg += f"{job_name}_run_number_{job_counter} field: {check_name}: {value_}\n"

    for check, value in files_check_list.items():
        if not value:
            e_msg += f"{check}: {value}\n"

    # Assert
    try:
        assert_db_fields(db_check_list)
        assert_files_recovered(files_check_list)
    except AssertionError:
        pytest.fail(e_msg)

    # TODO: GITLAB pipeline is not returning 0 or 1 for check_exit_code(final_status, exit_code)
    # assert_exit_code(final_status, exit_code)


@pytest.mark.parametrize("jobs_data, expected_db_entries, final_status, wrapper_type", [
    # Success
    ("""
    EXPERIMENT:
        NUMCHUNKS: '3'
    JOBS:
        job:
            SCRIPT: |
                echo "Hello World with id=Success"
                sleep 1
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01
    """, 3, "COMPLETED", "simple"),  # No wrappers, simple type
    # Success wrapper
    ("""
    EXPERIMENT:
        NUMCHUNKS: '2'
    JOBS:
        job:
            SCRIPT: |
                echo "Hello World with id=Success + wrappers"
                sleep 5
            DEPENDENCIES: job-1
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01
        job2:
            SCRIPT: |
                echo "Hello World with id=Success + wrappers"
                sleep 1
            DEPENDENCIES: job2-1
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01
    wrappers:
        wrapper:
            JOBS_IN_WRAPPER: job
            TYPE: vertical
        wrapper2:
            JOBS_IN_WRAPPER: job2
            TYPE: vertical
    """, 4, "COMPLETED", "vertical"),  # Wrappers present, vertical type
    # Failure
    ("""
    JOBS:
        job:
            SCRIPT: |
                sleep 1
                decho "Hello World with id=FAILED"
            PLATFORM: local
            RUNNING: chunk
            wallclock: 00:01
            retrials: 2  # In local, it started to fail at 18 retrials.
    """, (2 + 1) * 3, "FAILED", "simple"),  # No wrappers, simple type
    # Failure wrappers
    ("""
    JOBS:
        job:
            SCRIPT: |
                sleep 1
                decho "Hello World with id=FAILED + wrappers"
            PLATFORM: local
            DEPENDENCIES: job-1
            RUNNING: chunk
            wallclock: 00:10
            retrials: 2
    wrappers:
        wrapper:
            JOBS_IN_WRAPPER: job
            TYPE: vertical
    """, (2 + 1) * 1, "FAILED", "vertical"),  # Wrappers present, vertical type
], ids=["Success", "Success with wrapper", "Failure", "Failure with wrapper"])
def test_run_interrupted(run_tmpdir, prepare_run, jobs_data, expected_db_entries, final_status, wrapper_type, mocker):
    mocked_input = mocker.patch('autosubmit.autosubmit.input')
    mocked_input.side_effect = ['yes']
    from time import sleep
    log_dir = init_run(run_tmpdir, jobs_data)
    # Run the experiment
    exit_code = Autosubmit.run_experiment(expid='t000')
    assert exit_code == 0 if final_status != 'FAILED' else 1
    sleep(2)
    Autosubmit.stop(all_expids=False, cancel=False, current_status='SUBMITTED, QUEUING, RUNNING', expids='t000',
                    force=True, force_all=False, status='FAILED')
    Autosubmit.run_experiment(expid='t000')
    # Check and display results
    db_check_list = check_db_fields(run_tmpdir, expected_db_entries, final_status, wrapper_type)
    files_check_list = check_files_recovered(run_tmpdir, log_dir, expected_files=expected_db_entries * 2)

    # Assert
    assert_db_fields(db_check_list)
    assert_files_recovered(files_check_list)
    # TODO: GITLAB pipeline is not returning 0 or 1 for check_exit_code(final_status, exit_code)
    # assert_exit_code(final_status, exit_code)
