from ...sunra_schema import TextToVideoInput
from .schema import ReplicateInput


class TextToVideoMapper:    
    @staticmethod
    def convert(data: dict, skip_validation=True) -> dict:
        # Validate the input data if required
        if not skip_validation:
            input_model = TextToVideoInput.model_validate(data)
        else:
            input_model = TextToVideoInput.model_construct(**data)
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            frame_num=input_model.number_of_frames,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            aspect_ratio=input_model.aspect_ratio,
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True) 