import sys

import sentry_sdk
from gql import gql
from gql.transport.exceptions import TransportQueryError

from trail.exception.trail import RemoteTrailException, TrailUnavailableException
from trail.libconfig import is_development_environment
from trail.userconfig import userconfig
from trail.util.gql_client import build_gql_client

ADD_TEST_RESULT_MUTATIONS = """
mutation UpdateExperiment($experimentId: String!, $junitXml: String) {
  updateExperiment(
    experimentId: $experimentId,
    junitXml: $junitXml,
    hypothesis: null,
    coverageXml: null
    ) {
    experiment {
      id
    }
  }
}
 """


def add_test_results(junit_xml_path: str) -> list[str]:
    """Call the GraphQL mutation to add test results to an experiment.

    Args:
        junit_xml_path (str): The path to the JUnit XML file.

    """
    experiment_id = userconfig().project().parent_experiment_id
    with open(junit_xml_path, "r") as file:
        junit_xml = file.read()
    variables = {
        "junitXml": junit_xml,
        "experimentId": experiment_id,
    }
    client = build_gql_client()
    try:
        response = client.execute(
            document=gql(ADD_TEST_RESULT_MUTATIONS),
            variable_values=variables,
        )
        return response["updateExperiment"]["experiment"]["id"]

    except TransportQueryError as e:
        if is_development_environment():
            raise RemoteTrailException(
                "Could not upload pytest results in terra"
            ) from e
        else:
            sentry_sdk.capture_exception(e)
            print(TrailUnavailableException().message, file=sys.stderr)
