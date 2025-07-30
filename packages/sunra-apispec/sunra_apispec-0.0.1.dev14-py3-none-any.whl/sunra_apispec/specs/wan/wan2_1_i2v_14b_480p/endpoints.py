import os
from ....base.base_api_service import BaseAPIService, SubmitResponse
from ....base.output_schema import VideosOutput
from ......base.adapter_interface import ServiceProviderEnum
from ....model_mapping import model_mapping
from .sunra_schema import Image2VideoInput
from .service_providers.replicate.adapter import ImageToVideoAdapter as ReplicateImageToVideoAdapter


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Wan Video API",
    description="API for Wan 2.1 14B 480p Image-to-Video generation model",
    version="1.0.0",
    output_schema=VideosOutput,
)

@service.app.post(
    f"/{model_path}/image-to-video",
    response_model=SubmitResponse,
    description="Generate videos from images",
)
def image_to_video(body: Image2VideoInput) -> SubmitResponse:
    pass


registry_items = {
    f"{model_path}/image-to-video": [
        {
            "service_provider": ServiceProviderEnum.REPLICATE.value,
            "adapter": ReplicateImageToVideoAdapter,
        }
    ]
}
