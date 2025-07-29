import warnings
import os

from trail.userconfig.config import MainConfig

# Suppress all warnings -- mlflow produces ugly pydantic warnings rn
warnings.filterwarnings("ignore")

import argparse
import traceback

import sentry_sdk

from trail import libconfig
from trail.exception.trail import RemoteTrailException
from trail.userconfig.init import (
    init_environment,
)
from trail.util import auth, uploads
from trail.util.add_test_coverage_results import add_test_coverage_results
from trail.util.add_test_results import add_test_results
from trail.util.new_experiment import add_new_experiment
from trail.util.upload_artifacts_from_notebook import upload_artifacts_from_notebook
from trail.userconfig.config_utils import set_project, set_experiment


def handle_exception(e: Exception):
    if libconfig.is_development_environment():
        traceback.print_exc()
    else:
        sentry_sdk.capture_exception(e)

    print(e)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Trail CLI")
    parser.add_argument(
        "--upload-folder",
        "-u",
        required=False,
        help="Upload the specified folder to trail",
    )

    parser.add_argument(
        "--upload-file", "-f", required=False, help="Upload the specified file to trail"
    )

    parser.add_argument(
        "--upload-artifact-context",
        "-b",
        required=False,
        help="Add artifact context that where generated during a run to the indexer",
    )

    parser.add_argument(
        "--upload-notebook-artifact",
        "-a",
        required=False,
        help="Upload the jupyter notebook to trail and add outputs as artifacts",
    )

    parser.add_argument(
        "--add-pytest-results",
        "-t",
        required=False,
        help="Upload the specified junit xml formatted file to trail",
    )

    parser.add_argument(
        "--add-test-coverage-results",
        "-c",
        required=False,
        help="Upload the specified xml coverage file to trail",
    )

    parser.add_argument(
        "--set-project",
        "-p",
        required=False,
        help='Set the current project. Use "select" for interactive selection.',
    )

    parser.add_argument(
        "--set-experiment",
        "-e",
        required=False,
        help='Set the current experiment ID. Use "select" for interactive selection, or provide an experiment ID directly.',
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "init",
        help="Initialize a new trail environment. "
        "This will create a new configuration file in the current directory.",
    )

    subparsers.add_parser("add-new-experiment", help="Add a new experiment to trail")

    args = parser.parse_args()

    if args.command == "init":
        try:
            init_environment()
        except RemoteTrailException as e:
            handle_exception(e)
        return
    elif args.command == "add-new-experiment":
        try:
            add_new_experiment()
        except RemoteTrailException as e:
            handle_exception(e)
        return
    else:
        try:
            if args.set_project:
                interactive = args.set_project.lower() == "select"
                project_id = set_project(
                    None if interactive else args.set_project, interactive=interactive
                )
                print(f"Project ID set to: {project_id}")
                print("Experiment updated successfully.")
                return

            if args.set_experiment:
                interactive = args.set_experiment.lower() == "select"
                experiment_id = set_experiment(
                    None if interactive else args.set_experiment,
                    interactive=interactive,
                )
                print(f"Experiment ID set to: {experiment_id}")
                return

            if args.upload_file:
                print(f"Uploading file: {args.upload_file}")
                try:
                    uploads.upload_file(
                        args.upload_file,
                        tasks=[uploads.NebulaTaskType.CHUNK_EMBEDDING.name],
                    )
                except RemoteTrailException as e:
                    handle_exception(e)
            elif args.upload_artifact_context:
                print(f"Uploading artifact context: {args.upload_artifact_context}")
                try:
                    uploads.upload_file(
                        args.upload_artifact_context,
                        tasks=[uploads.NebulaTaskType.ARTIFACT_CONTEXT_INDEXING.name],
                    )
                except RemoteTrailException as e:
                    handle_exception(e)
            elif args.upload_folder:
                try:
                    uploads.upload_folder(args.upload_folder)
                except RemoteTrailException as e:
                    handle_exception(e)
                except FileNotFoundError as e:
                    print(e)
            elif args.upload_notebook_artifact:
                print(f"Uploading notebook artifact: {args.upload_notebook_artifact}")
                try:
                    uploads.upload_file(
                        args.upload_notebook_artifact,
                        tasks=[
                            uploads.NebulaTaskType.JUPYTER_NOTEBOOK_CELL_OUTPUT_INDEXING.name
                        ],
                    )
                    upload_artifacts_from_notebook(args.upload_notebook_artifact)
                except RemoteTrailException as e:
                    handle_exception(e)
            elif args.add_pytest_results:
                print(f"Uploading pytest results: {args.add_pytest_results}")
                try:
                    add_test_results(args.add_pytest_results)
                except RemoteTrailException as e:
                    handle_exception(e)
            elif args.add_test_coverage_results:
                print(
                    f"Uploading test coverage results: {args.add_test_coverage_results}"
                )
                try:
                    add_test_coverage_results(args.add_test_coverage_results)
                except RemoteTrailException as e:
                    handle_exception(e)
            else:
                parser.print_help()
        except RemoteTrailException as e:
            handle_exception(e)
            return
        except ValueError as e:
            print(str(e))
            return


def main():
    parse_arguments()


if __name__ == "__main__":
    main()
