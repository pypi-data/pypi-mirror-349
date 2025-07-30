import os
from base.base_api_service import BaseAPIService, SubmitResponse
from base.output_schema import ImagesOutput
from model_mapping import model_mapping
from .sunra_schema import Text2ImageInput


model_name = os.path.basename(os.path.dirname(__file__))
model_provider = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
model_path = model_mapping[f"{model_provider}/{model_name}"]


service = BaseAPIService(
    title="Luma Photon Flash API",
    description="API for Luma Photon Flash high-quality image generation model - Accelerated variant of Photon prioritizing speed while maintaining quality.",
    version="1.0.0",
    output_schema=ImagesOutput,
)

@service.app.post(
    f"/{model_path}/text-to-image",
    response_model=SubmitResponse,
    description="Generate image from text prompts",
)
def text_to_image(body: Text2ImageInput) -> SubmitResponse:
    pass
