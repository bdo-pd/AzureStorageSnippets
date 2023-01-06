import os, uuid
import time
from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobLeaseClient

class ContainerSamples(object):

    # <Snippet_create_container>
    def create_blob_container(self, blob_service_client: BlobServiceClient, container_name):
        try:
            container_client = blob_service_client.create_container(name=container_name)
        except ResourceExistsError:
            print('A container with this name already exists')
    # </Snippet_create_container>

    # <Snippet_create_root_container>
    def create_blob_root_container(self, blob_service_client: BlobServiceClient):
        container_client = blob_service_client.get_container_client(name="$root")
        container_client.create_container()
    # </Snippet_create_root_container>

    # <Snippet_list_containers>
    def list_containers(self, blob_service_client: BlobServiceClient):
        all_containers = blob_service_client.list_containers(include_metadata=True)
        for container in all_containers:
            print(container['name'], container['metadata'])
    # </Snippet_list_containers>

    # <Snippet_list_containers_prefix>
    def list_containers_prefix(self, blob_service_client: BlobServiceClient):
        containers = blob_service_client.list_containers(name_starts_with='test-')
        for container in containers:
            print(container['name'], container['metadata'])
    # </Snippet_list_containers_prefix>

    # <Snippet_acquire_container_lease>
    def acquire_container_lease(self, blob_service_client: BlobServiceClient, container_name):
        # Instantiate a ContainerClient
        container_client = blob_service_client.get_container_client(container_name)

        # Acquire a 30-second lease on the container
        lease_client = container_client.acquire_lease(30)

        return lease_client
    # </Snippet_acquire_container_lease>

    # <Snippet_renew_container_lease>
    def renew_container_lease(self, lease_client: BlobLeaseClient):
        # Renew a lease on the container
        lease_client.renew()
    # </Snippet_renew_container_lease>

    # <Snippet_release_container_lease>
    def release_container_lease(self, lease_client: BlobLeaseClient):
        # Release a lease on the container
        lease_client.release()
    # </Snippet_release_container_lease>

    # <Snippet_break_container_lease>
    def break_container_lease(self, lease_client: BlobLeaseClient):
        # Break a lease on the container
        lease_client.break_lease()
    # </Snippet_break_container_lease>

    def container_properties_metadata(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)

        properties = container_client.get_container_properties()

        print(f"Public access type: {properties.public_access}")
        print(f"Lease status: {properties.lease.status}")
        print(f"Lease state: {properties.lease.state}")
        print(f"Has immutability policy: {properties.has_immutability_policy}")

    # <Snippet_delete_container>
    def delete_container(self, blob_service_client: BlobServiceClient, container_name):
        container_client = blob_service_client.get_container_client(container=container_name)
        container_client.delete_container()
    # </Snippet_delete_container>

    # <Snippet_delete_container_prefix>
    def delete_container(self, blob_service_client: BlobServiceClient):
        container_list = list(blob_service_client.list_containers(name_starts_with="test-"))
        assert len(container_list) >= 1

        for container in container_list:
            # Find containers with the specified prefix and delete
            container_client = blob_service_client.get_container_client(container=container.name)
            container_client.delete_container()
    # </Snippet_delete_container_prefix>

    # <Snippet_restore_container>
    def restore_deleted_container(self, blob_service_client: BlobServiceClient, container_name):
        container_list = list(blob_service_client.list_containers(include_deleted=True))
        assert len(container_list) >= 1

        for container in container_list:
            # Find the deleted container and restore it
            if container.deleted and container.name == container_name:
                restored_container_client = blob_service_client.undelete_container(container.name, container.version)
    # </Snippet_restore_container>

if __name__ == '__main__':
    # TODO: Replace <storage-account-name> with your actual storage account name
    account_url = "https://<storage-account-name>.blob.core.windows.net"
    credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=credential)

    sample = ContainerSamples()
    sample.create_blob_container(blob_service_client, "sample-container")
    sample.list_containers(blob_service_client)
    sample.list_containers_prefix(blob_service_client)
    lease_client = sample.acquire_container_lease(blob_service_client, "sample-container")
    sample.renew_container_lease(lease_client)
    sample.release_container_lease(lease_client)
    sample.break_container_lease(lease_client)
    sample.container_properties_metadata(blob_service_client, "sample-container")
    sample.delete_container(blob_service_client, "sample-container")
    #sample.restore_deleted_container(blob_service_client, "sample-container")