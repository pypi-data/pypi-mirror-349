import re
import requests

from datetime import datetime, timezone

from unity_sds_client.unity_exception import UnityException
from unity_sds_client.unity_session import UnitySession
from unity_sds_client.resources.collection import Collection
from unity_sds_client.resources.dataset import Dataset
from unity_sds_client.resources.data_file import DataFile

# All capitals to match the unity-dataservices stage-out convention
UNITY_COLLECTION_INVARIANT_PREFIX = "URN:NASA:UNITY"

class DataService(object):
    """
    The DataService class is a wrapper to the data endpoint(s) within Unity. This wrapper interfaces with the DAPA endpoints.

    The DataService class allows for the querying of data collections and data files within those collections.
    """

    def __init__(
        self,
        session: UnitySession,
        endpoint: str = None,
    ):
        """Initialize the DataService class.

        Parameters
        ----------
        session : UnitySession
            Description of parameter `session`.
        endpoint : str
            The endpoint used to access the data service API. This is usually
            shared across Unity Environments, but can be overridden. Defaults to
            "None", and will be read from the configuration if not set.

        Returns
        -------
        DataService
            the Data Service object.

        """
        self._session = session
        if endpoint is None:
            self.endpoint = self._session.get_unity_href()

    def get_collections(self, limit=10, output_stac=False):
        """Returns a list of collections

        Returns
        -------
        list
            List of returned collections

        """
        url = self.endpoint + "am-uds-dapa/collections"
        token = self._session.get_auth().get_token()
        response = requests.get(url, headers={"Authorization": "Bearer " + token}, params={"limit": limit})
        if output_stac:
            return response.json()

        # build collection objects here
        collections = []
        for data_set in response.json()['features']:
            collections.append(Collection(data_set['id']))

        return collections

    def get_collection_data(self, collection: type = Collection, limit=10, filter: str = None, output_stac=False):
        datasets = []
        url = self.endpoint + f'am-uds-dapa/collections/{collection.collection_id}/items'
        token = self._session.get_auth().get_token()
        params = {"limit": limit}
        if filter is not None:
            params["filter"] = filter
        response = requests.get(url, headers={"Authorization": "Bearer " + token}, params=params)
        if output_stac:
            return response.json()
        results = response.json()['features']
        
        for dataset in results:
            ds = Dataset(dataset['id'], collection.collection_id, dataset['properties']['start_datetime'], dataset['properties']['end_datetime'], dataset['properties']['created'], properties=dataset['properties'])

            for asset_key in dataset['assets']:
                location = dataset['assets'][asset_key]['href']
                file_type = dataset['assets'][asset_key].get('type', "")
                title = dataset['assets'][asset_key].get('title', "")
                description = dataset['assets'][asset_key].get('description', "")
                roles = dataset['assets'][asset_key]["roles"] if "roles" in dataset['assets'][asset_key] else ["metadata"] if asset_key in ['metadata__cmr','metadata__data'] else [asset_key]
                ds.add_data_file(DataFile(file_type, location, roles=roles, title=title, description=description))

            datasets.append(ds)

        return datasets

    def create_collection(self, collection: type = Collection, dry_run=False):

        # Collection must not be None
        if collection is None:
            raise UnityException("Invalid collection provided.")

        # Test collection ID name: project and venue
        if self._session._project is None or self._session._venue is None:
            raise UnityException("To create a collection, the Unity session Project and Venue must be set!")

        # Enusure the collection ID contains a prefix that conforms to expectations, testing in a case insensitive manner
        # But promoting to the preferred case
        submission_collection_id = collection.collection_id

        if not re.search(rf'^{UNITY_COLLECTION_INVARIANT_PREFIX}', submission_collection_id, re.IGNORECASE):
            raise UnityException(f"Collection Identifiers must start with {UNITY_COLLECTION_INVARIANT_PREFIX}")

        # Make the prefix conform to expected formatting (case) to ensure consistency across services
        submission_collection_id = re.sub(rf'^{UNITY_COLLECTION_INVARIANT_PREFIX}', UNITY_COLLECTION_INVARIANT_PREFIX, submission_collection_id, flags=re.IGNORECASE)

        if not submission_collection_id.startswith(f"{UNITY_COLLECTION_INVARIANT_PREFIX}:{self._session._project}:{self._session._venue}"):
            raise UnityException(f"Collection Identifiers must start with {UNITY_COLLECTION_INVARIANT_PREFIX}:{self._session._project}:{self._session._venue}")

        collection_json = {
            "title": "Collection " + submission_collection_id,
            "type": "Collection",
            "id": submission_collection_id,
            "stac_version": "1.0.0",
            "description": "Collection " + submission_collection_id,
            "providers": [
                {"name": "unity"}
            ],
            "links": [],
            "stac_extensions": [],
            "extent": {
                "spatial": {
                    "bbox": [
                        [
                            0,
                            0,
                            0,
                            0
                        ]
                    ]
                },
                "temporal": {
                    "interval": [
                        [
                            datetime.now(timezone.utc).isoformat(),
                            datetime.now(timezone.utc).isoformat()
                        ]
                    ]
                }
            },
            "license": "proprietary",
            "summaries": {
                "granuleId": [
                    "^test_file.*$"
                ],
                "granuleIdExtraction": [
                    "(^test_file.*)(\\.nc|\\.nc\\.cas|\\.cmr\\.xml)"
                ],
                "process": [
                    "stac"
                ]
            }
        }
        if not dry_run:
            url = self.endpoint + f'am-uds-dapa/collections'
            token = self._session.get_auth().get_token()
            response = requests.post(url, headers={"Authorization": "Bearer " + token},  json=collection_json)

            if response.status_code != 202:
                raise UnityException(f"Error creating collection: " + response.text)

        return collection_json

    def define_custom_metadata(self, metadata: dict):
        if self._session._project is None or self._session._venue is None:
            raise UnityException("To add custom metadata, the Unity session Project and Venue must be set!")

        url = self.endpoint + f'am-uds-dapa/admin/custom_metadata/{self._session._project}'
        token = self._session.get_auth().get_token()
        response = requests.put(url, headers={"Authorization": "Bearer " + token},
                                params={"venue": self._session._venue}, json=metadata)
        if response.status_code != 200:
            raise UnityException("Error adding custom metadata: " + response.text)

    def delete_collection_item(self, collection: type = Collection, granule_id: str = None):
        """
            Delete a granule from given a collection
            Parameters
            -------
            collection: Collection
                The collection object associated to the granule to delete
            granule_id: String
                The granule id to delete

    	""" 
        if (granule_id == "") or (granule_id is None):
            raise Exception("Error deleting collection data: Please provide granule ID")

        else:
            url = f'{self.endpoint}am-uds-dapa/collections/{collection.collection_id}/items/{granule_id}/'        
            token = self._session.get_auth().get_token()        
            header = {"Authorization": f"Bearer {token}"}
            response = requests.delete(url=url, headers=header)
            print(response.status_code)
            if response.status_code != 200:
                raise UnityException("Error deleting collection: " + response.reason)   

    def delete_dataset(self, dataset: type = Dataset):
        """
            Delete an item from a Collection given Dataset object  
            Parameters
            ----------
            dataset: Dataset
        """
    
        self.delete_collection_item(Collection(dataset.collection_id), dataset.id)
