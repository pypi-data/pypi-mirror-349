from ...input_schema import TextToVideoInput
from .schema import ReplicateInput


class Wan2_1_T2V_1_3B_480PReplicateMapper:    
    @staticmethod
    def validate_and_convert_text_to_video_input(data: dict) -> dict:
        # Validate the input data
        input_model = TextToVideoInput.model_validate(data)
        
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