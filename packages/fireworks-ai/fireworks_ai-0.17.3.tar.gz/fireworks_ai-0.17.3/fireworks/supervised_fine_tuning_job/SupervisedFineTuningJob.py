import asyncio
from datetime import datetime
from typing import Optional
from fireworks.gateway import Gateway
from fireworks.dataset import Dataset
from fireworks.control_plane.generated.protos.gateway import (
    CreateSupervisedFineTuningJobRequest,
    JobState,
    Region,
    SupervisedFineTuningJob as SupervisedFineTuningJobProto,
    ListSupervisedFineTuningJobsRequest,
    SupervisedFineTuningJobWeightPrecision,
    WandbConfig,
    AcceleratorType as AcceleratorTypeEnum,
)
from fireworks.llm import LLM


class SupervisedFineTuningJob:
    """
    Wrapper around proto for a supervised fine-tuning job in Fireworks. Can be
    constructed from a name, LLM, and dataset. Can be used to sync the job state
    to Fireworks and query the current state.
    """

    def __init__(
        self,
        name: str,
        llm: LLM,
        dataset: Dataset,
        api_key: Optional[str] = None,
        epochs: Optional[int] = None,
        learning_rate: Optional[float] = None,
        lora_rank: Optional[int] = None,
        jinja_template: Optional[str] = None,
        early_stop: Optional[bool] = None,
        max_context_length: Optional[int] = None,
        base_model_weight_precision: Optional[SupervisedFineTuningJobWeightPrecision] = None,
        wandb_config: Optional[WandbConfig] = None,
        evaluation_dataset: Optional[str] = None,
        accelerator_type: Optional[AcceleratorTypeEnum] = None,
        accelerator_count: Optional[int] = None,
        is_turbo: Optional[bool] = None,
        eval_auto_carveout: Optional[bool] = None,
        region: Optional[Region] = None,
        nodes: Optional[int] = None,
        batch_size: Optional[int] = None,
        state: Optional[JobState] = None,
        create_time: Optional[datetime] = None,
        update_time: Optional[datetime] = None,
        created_by: Optional[str] = None,
        output_model: Optional[str] = None,
    ):
        self.name = name
        self.llm = llm
        self.dataset = dataset
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.lora_rank = lora_rank
        self.jinja_template = jinja_template
        self.early_stop = early_stop
        self.max_context_length = max_context_length
        self.base_model_weight_precision = base_model_weight_precision
        self.wandb_config = wandb_config
        self.evaluation_dataset = evaluation_dataset
        self.accelerator_type = accelerator_type
        self.accelerator_count = accelerator_count
        self.is_turbo = is_turbo
        self.eval_auto_carveout = eval_auto_carveout
        self.region = region
        self.nodes = nodes
        self.batch_size = batch_size
        self.state = state
        self.create_time = create_time
        self.update_time = update_time
        self.created_by = created_by
        self.output_model = output_model
        self._api_key = api_key
        self._gateway = Gateway(api_key=api_key)

    @classmethod
    async def delete_by_name(cls, name: str, api_key: Optional[str] = None):
        gateway = Gateway(api_key=api_key)
        await gateway.delete_supervised_fine_tuning_job(name)
        job = await gateway.get_supervised_fine_tuning_job(name)
        while job is not None:
            await asyncio.sleep(1)

    async def delete(self):
        await SupervisedFineTuningJob.delete_by_name(self.name, self._api_key)

    async def sync(self) -> "SupervisedFineTuningJob":
        """
        Creates the job if it doesn't exist, otherwise returns the existing job.
        """
        existing_job = await self.get()
        if existing_job is not None:
            return existing_job
        await self.dataset.sync()
        request = await self._create_request()
        await self._gateway.create_supervised_fine_tuning_job(request)
        new_job = await self.get()
        if new_job is None:
            raise ValueError(f"Failed to create supervised fine-tuning job {self.name}")
        return new_job

    async def _create_request(self) -> CreateSupervisedFineTuningJobRequest:
        dataset_id = await self.dataset.id()
        job_proto = SupervisedFineTuningJobProto(
            display_name=self.name,
            base_model=self.llm.model,
            dataset=dataset_id,
        )
        if self.epochs is not None:
            job_proto.epochs = self.epochs
        if self.learning_rate is not None:
            job_proto.learning_rate = self.learning_rate
        if self.lora_rank is not None:
            job_proto.lora_rank = self.lora_rank
        if self.jinja_template is not None:
            job_proto.jinja_template = self.jinja_template
        if self.early_stop is not None:
            job_proto.early_stop = self.early_stop
        if self.max_context_length is not None:
            job_proto.max_context_length = self.max_context_length
        if self.base_model_weight_precision is not None:
            job_proto.base_model_weight_precision = self.base_model_weight_precision
        if self.wandb_config is not None:
            job_proto.wandb_config = self.wandb_config
        if self.evaluation_dataset is not None:
            job_proto.evaluation_dataset = self.evaluation_dataset
        if self.accelerator_type is not None:
            job_proto.accelerator_type = self.accelerator_type
        if self.accelerator_count is not None:
            job_proto.accelerator_count = self.accelerator_count
        if self.is_turbo is not None:
            job_proto.is_turbo = self.is_turbo
        if self.eval_auto_carveout is not None:
            job_proto.eval_auto_carveout = self.eval_auto_carveout
        if self.region is not None:
            job_proto.region = self.region
        if self.nodes is not None:
            job_proto.nodes = self.nodes
        if self.batch_size is not None:
            job_proto.batch_size = self.batch_size
        if self.output_model is not None:
            job_proto.output_model = self.output_model
        request = CreateSupervisedFineTuningJobRequest(
            supervised_fine_tuning_job=job_proto,
        )
        return request

    async def get(self) -> Optional["SupervisedFineTuningJob"]:
        """
        TODO: we should not be using display_name to find the job, but instead
        the name. But due to a bug when reusing the same Job ID, we need to use
        display_name as our identifier.
        """
        request = ListSupervisedFineTuningJobsRequest()
        page_token = None
        while True:
            if page_token is not None:
                request.page_token = page_token
            list_response = await self._gateway.list_supervised_fine_tuning_jobs(request)
            for job_proto in list_response.supervised_fine_tuning_jobs:
                if job_proto.display_name == self.name:
                    return SupervisedFineTuningJob(
                        name=job_proto.display_name,
                        llm=self.llm,
                        dataset=self.dataset,
                        api_key=self._api_key,
                        state=job_proto.state,
                        epochs=job_proto.epochs,
                        learning_rate=job_proto.learning_rate,
                        lora_rank=job_proto.lora_rank,
                        jinja_template=job_proto.jinja_template,
                        early_stop=job_proto.early_stop,
                        max_context_length=job_proto.max_context_length,
                        base_model_weight_precision=job_proto.base_model_weight_precision,
                        wandb_config=job_proto.wandb_config,
                        evaluation_dataset=job_proto.evaluation_dataset,
                        accelerator_type=job_proto.accelerator_type,
                        accelerator_count=job_proto.accelerator_count,
                        is_turbo=job_proto.is_turbo,
                        eval_auto_carveout=job_proto.eval_auto_carveout,
                        region=job_proto.region,
                        nodes=job_proto.nodes,
                        batch_size=job_proto.batch_size,
                        create_time=job_proto.create_time,
                        update_time=job_proto.update_time,
                        created_by=job_proto.created_by,
                        output_model=job_proto.output_model,
                    )
            if not list_response.next_page_token:
                return None
            page_token = list_response.next_page_token
