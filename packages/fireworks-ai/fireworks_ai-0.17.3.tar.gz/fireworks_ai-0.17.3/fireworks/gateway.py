# Copyright (c) Fireworks AI, Inc. and affiliates.
#
# All Rights Reserved.

import os
from typing import List, Optional, TypeVar, Union

import grpclib
from grpclib.client import Channel
import httpx
from betterproto.lib.std.google.protobuf import FieldMask
from fireworks.control_plane.generated.protos.gateway import (
    AcceleratorType,
    AutoscalingPolicy,
    CreateDatasetRequest,
    CreateDeploymentRequest,
    CreateSupervisedFineTuningJobRequest,
    Dataset,
    DeleteDatasetRequest,
    DeleteSupervisedFineTuningJobRequest,
    Deployment,
    GatewayStub,
    GetDatasetUploadEndpointRequest,
    GetDeploymentRequest,
    GetSupervisedFineTuningJobRequest,
    ListDatasetsRequest,
    ListDeploymentsRequest,
    ListModelsRequest,
    ListModelsResponse,
    ListSupervisedFineTuningJobsRequest,
    ListSupervisedFineTuningJobsResponse,
    Model,
    ScaleDeploymentRequest,
    SupervisedFineTuningJob,
    UpdateDeploymentRequest,
    CreateDatasetValidationJobRequest,
    ValidateDatasetUploadRequest,
)
from asyncstdlib.functools import cache
from openai import NOT_GIVEN, NotGiven


def _get_api_key_from_env() -> Optional[str]:
    """
    Attempts to obtain API key from the environment variable.

    Returns:
        API key retrieved from env variable or None if missing.
    """
    return os.environ.get("FIREWORKS_API_KEY")


R = TypeVar("R")


class Gateway:
    """
    Control plane gateway client that exposes its endpoints through
    convenient APIs.

    Keep the API consistent with `gateway.proto`.
    """

    def __init__(
        self,
        *,
        server_addr: str = "gateway.fireworks.ai:443",
        api_key: Optional[str] = None,
    ) -> None:
        """
        Args:
            server_addr: the network address of the gateway server.
            api_key: the API key to use for authentication.
        """
        self._server_addr = server_addr
        if not api_key:
            api_key = _get_api_key_from_env()
            if not api_key:
                raise ValueError(
                    "Fireworks API key not found. Please provide an API key either as a parameter "
                    "or by setting the FIREWORKS_API_KEY environment variable. "
                    "You can create a new API key at https://fireworks.ai/settings/users/api-keys or "
                    "by using `firectl create api-key --key-name <key-name>` command."
                )
        self._api_key = api_key
        self._host = self._server_addr.split(":")[0]
        self._port = int(self._server_addr.split(":")[1])
        self._channel = Channel(host=self._host, port=self._port, ssl=True)
        self._stub = GatewayStub(self._channel, metadata=[("x-api-key", api_key)])

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._channel.close()

    async def create_supervised_fine_tuning_job(
        self, request: CreateSupervisedFineTuningJobRequest
    ) -> SupervisedFineTuningJob:
        account_id = await self.account_id()
        request.parent = f"accounts/{account_id}"
        response = await self._stub.create_supervised_fine_tuning_job(request)
        return response

    async def delete_supervised_fine_tuning_job(self, name: str) -> None:
        account_id = await self.account_id()
        try:
            await self._stub.delete_supervised_fine_tuning_job(
                DeleteSupervisedFineTuningJobRequest(name=f"accounts/{account_id}/supervisedFineTuningJobs/{name}")
            )
        except grpclib.exceptions.GRPCError as e:
            if e.status == grpclib.Status.NOT_FOUND:
                return
            raise e

    async def list_supervised_fine_tuning_jobs(
        self, request: ListSupervisedFineTuningJobsRequest
    ) -> ListSupervisedFineTuningJobsResponse:
        account_id = await self.account_id()
        request.parent = f"accounts/{account_id}"
        request.page_size = 200
        response = await self._stub.list_supervised_fine_tuning_jobs(request)
        return response

    async def get_supervised_fine_tuning_job(self, name: str) -> Optional[SupervisedFineTuningJob]:
        account_id = await self.account_id()
        try:
            response = await self._stub.get_supervised_fine_tuning_job(
                GetSupervisedFineTuningJobRequest(name=f"accounts/{account_id}/supervisedFineTuningJobs/{name}")
            )
            return response
        except grpclib.exceptions.GRPCError as e:
            if e.status == grpclib.Status.NOT_FOUND:
                return None
            raise e

    async def list_datasets(
        self,
        request: ListDatasetsRequest,
    ) -> List[Dataset]:
        account_id = await self.account_id()
        request.parent = f"accounts/{account_id}"
        response = await self._stub.list_datasets(request)
        return response.datasets

    async def delete_dataset(self, name: str) -> None:
        account_id = await self.account_id()
        await self._stub.delete_dataset(DeleteDatasetRequest(name=f"accounts/{account_id}/datasets/{name}"))

    async def validate_dataset(self, name: str) -> None:
        account_id = await self.account_id()
        await self._stub.validate_dataset_upload(
            ValidateDatasetUploadRequest(name=f"accounts/{account_id}/datasets/{name}")
        )

    async def create_dataset(
        self,
        request: CreateDatasetRequest,
    ) -> Dataset:
        account_id = await self.account_id()
        request.parent = f"accounts/{account_id}"
        response = await self._stub.create_dataset(request)
        return response

    async def get_dataset_upload_endpoint(
        self,
        name: str,
        filename_to_size: dict[str, int],
    ) -> dict[str, str]:
        account_id = await self.account_id()
        name = f"accounts/{account_id}/datasets/{name}"
        response = await self._stub.get_dataset_upload_endpoint(
            GetDatasetUploadEndpointRequest(name=name, filename_to_size=filename_to_size)
        )
        return response.filename_to_signed_urls

    async def list_models(
        self,
        *,
        parent: str = "",
        filter: str = "",
        order_by: str = "",
        include_deployed_model_refs: bool = False,
    ) -> List[Model]:
        """
        Paginates through the list of available models and returns all of them.

        Args:
            parent: resource name of the parent account,
            filter: only models satisfying the provided filter (if specified)
                will be returned. See https://google.aip.dev/160 for the filter
                grammar,
            order_by: a comma-separated list of fields to order by. e.g. "foo,bar".
                The default sort order is ascending. To specify a descending order
                for a field, append a " desc" suffix. e.g. "foo desc,bar"
                Subfields are specified with a "." character. e.g. "foo.bar".
                If not specified, the default order is by "name".

        Returns:
            list of models satisfying the retrieval criteria.
        """
        result = []
        page_token = None
        while True:
            request = ListModelsRequest(
                parent=parent,
                filter=filter,
                order_by=order_by,
                include_deployed_model_refs=include_deployed_model_refs,
                page_size=200,
            )
            if page_token is not None:
                request.page_token = page_token
            response: ListModelsResponse = await self._stub.list_models(request)
            result.extend(response.models)
            if response.total_size < len(result):
                return result
            elif response.total_size == len(result):
                return result
            page_token = response.next_page_token

    async def list_deployments(self, filter: str = ""):
        account_id = await self.account_id()
        deployments = await self._stub.list_deployments(
            ListDeploymentsRequest(parent=f"accounts/{account_id}", filter=filter)
        )
        return deployments.deployments

    async def create_deployment(
        self,
        deployment: Deployment,
    ):
        account_id = await self.account_id()
        request = CreateDeploymentRequest(parent=f"accounts/{account_id}", deployment=deployment)
        created_deployment = await self._stub.create_deployment(request)
        return created_deployment

    async def scale_deployment(self, name: str, replicas: int):
        await self._stub.scale_deployment(ScaleDeploymentRequest(name=name, replica_count=replicas))

    async def update_deployment(
        self,
        name: str,
        autoscaling_policy: Optional[AutoscalingPolicy] = None,
        accelerator_type: Optional[AcceleratorType] = None,
    ):
        deployment = Deployment(name=name)
        update_mask = FieldMask(paths=[])
        if autoscaling_policy is not None:
            deployment.autoscaling_policy = autoscaling_policy
            update_mask.paths.append("autoscaling_policy")
        if accelerator_type is not None:
            deployment.accelerator_type = accelerator_type
            update_mask.paths.append("accelerator_type")
        if len(update_mask.paths) == 0:
            return
        await self._stub.update_deployment(UpdateDeploymentRequest(deployment=deployment, update_mask=update_mask))

    async def get_deployment(self, name: str) -> Deployment:
        return await self._stub.get_deployment(GetDeploymentRequest(name=name))

    @cache
    async def account_id(self) -> str:
        # make curl -v -H "Authorization: Bearer XXX" https://api.fireworks.ai/verifyApiKey
        # and read x-fireworks-account-id from headers of the response
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.fireworks.ai/verifyApiKey",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                },
            )
            return response.headers["x-fireworks-account-id"]
