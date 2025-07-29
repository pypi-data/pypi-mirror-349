import traceback

import requests
from unity_sps_ogc_processes_api_python_client.models.execute200_response_input import Execute200ResponseInput
from unity_sps_ogc_processes_api_python_client.models.execute_workflows import ExecuteWorkflows
from unity_sps_ogc_processes_api_python_client.exceptions import NotFoundException

from unity_sds_client.resources.job_status import JobStatus
from unity_sds_client.unity_exception import UnityException
from unity_sds_client.unity_session import UnitySession
from unity_sds_client.resources.job import Job
import unity_sps_ogc_processes_api_python_client
from unity_sps_ogc_processes_api_python_client.rest import ApiException
from unity_sps_ogc_processes_api_python_client.models.process_list import ProcessList


class Process(object):

    def __str__(self):
        return '''unity_sds_client.resources.Process(
    id="{}",
    process_version="{}"
    title="{}",
    abstract="{}",
    keywords="{}"
)'''.format(
            self.id,
            self.process_version,
            self.title,
            self.abstract,
            self.keywords
        )

    def __init__(
            self,
            session: UnitySession,
            endpoint: str,
            process_id: str,
            title: str,
            abstract: str,
            process_version: str,
            keywords: str,
            job_control_options: list,
            inputs: object = None,
            outputs: object = None,
    ):
        """
        Initialize the Process class.

        Parameters
        ----------
        session : UnitySession
            The Unity Session that will be used to facilitate making calls to the SPS endpoints.
        endpoint : str
            The endpoint to call for executing processes

        Returns
        -------
        Process
            The Process object.

        """
        self._session = session
        self._endpoint = endpoint
        self.id = process_id
        self.title = title
        self.job_control_options = job_control_options
        self.keywords = keywords
        self.process_version = process_version
        self.abstract = abstract
        self.inputs = inputs
        self.outputs = outputs

    def execute(self, data) -> Job:
        '''

        @param data:
        @return Job:
        '''

        token = self._session.get_auth().get_token()
        url = self._endpoint
        configuration = unity_sps_ogc_processes_api_python_client.Configuration(
            host=url,
            access_token=token
        )
        with unity_sps_ogc_processes_api_python_client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = unity_sps_ogc_processes_api_python_client.ProcessesApi(api_client)
            process_id = self.id
            response = None
            prefer = "respond-async" # TODO should be an argument
            execute_workflows = ExecuteWorkflows.from_dict(data)
            try:
                api_response = api_instance.execute_processes_process_id_execution_post(
                    process_id,
                    response=response,
                    prefer=prefer,
                    execute_workflows=execute_workflows,
                ) # add auth
                api_response_dict = {key: value for key, value in api_response.anyof_schema_2_validator}
                return Job(
                            self._session,
                            self._endpoint,
                            api_response_dict["process_id"],
                            api_response_dict["job_id"],
                            JobStatus(api_response_dict["status"])
                    )

            except NotFoundException as nfe:
                raise UnityException(nfe.body)
            except Exception as e:
                print(traceback.format_exc())
                print("Exception when calling ProcessesApi->execute_processes_process_id_execution_post: %s\n" % e)
                raise UnityException(e.body)
