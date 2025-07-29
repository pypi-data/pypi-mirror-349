"""
The HealthService module contains those utilities related to the 
Unity Health Services Infrastructure.
"""

import requests
from unity_sds_client.unity_session import UnitySession
from unity_sds_client.utils.http import get_headers

class HealthService(object):
    """
    The HealthService class is a wrapper to Unity's Health API endpoints.
    """

    def __init__(
        self,
        session:UnitySession,
        endpoint: str = None
    ):
        """
        Initialize the HealthService class.

        Parameters
        ----------
        session : UnitySession
            The Unity Session that will be used to facilitate making calls to the Health endpoints.

        Returns
        -------
        List
            List of applications and their health statses
        """

        self._session = session
        if endpoint is None:
            self.endpoint = self._session.get_unity_href()

    def __str__(self):
        return self.generate_health_status_report()

    def get_health_status(self):
        """
        Returns a list of services and their respective health status
        """

        token = self._session.get_auth().get_token()
        project = self._session.get_project()
        venue = self._session.get_venue()
        url = self.endpoint + f"{project}/{venue}/management/api/health_checks"

        headers = get_headers(token, {
            'Content-type': 'application/json'
        })

        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.HTTPError as exception:
            raise exception

        return response.json()

    def generate_health_status_report(self):
        """
        Return a generated report of health status information
        """

        health_status_title = "HEALTH STATUS REPORT"
        report = f"\n\n{health_status_title}\n"
        report = report + len(health_status_title) * "-" + "\n\n"

        try:
            health_statuses = self.get_health_status()
        except requests.HTTPError as error:
            report = report + f"Error encountered with Health API Endpoint ({error.response.status_code})\n"
            return report

        for service in health_statuses["services"]:
            service_name = service["componentName"]
            service_category = service["componentCategory"]
            service_type = service["componentType"]
            service_description = service["description"]
            landing_page_url = service["landingPageUrl"]
            report = report + f"{service_name}\n"
            report = report + f"{service_description}\n"
            report = report + f"URL: {landing_page_url}\n"
            report = report + f"Category: {service_category}\n"
            report = report + f"Type: {service_type}\n"
            for status in service["healthChecks"]:
                service_status = status["status"]
                service_status_date = status["date"]
                report = report + f"Health Status as of {service_status_date}: {service_status}\n"
            report = report + "\n"

        return report

    def print_health_status(self):
        """
        Print the health status report
        """
        print(f"{self.generate_health_status_report()}")
