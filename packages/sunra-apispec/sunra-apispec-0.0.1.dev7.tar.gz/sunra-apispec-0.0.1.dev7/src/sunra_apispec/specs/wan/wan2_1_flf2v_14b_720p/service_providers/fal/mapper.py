from ...input_schema import ImageToVideoInput
from .schema import FalInput


class Wan2_1_FLF2V_14b_720PFalMapper:
    """Mapper class to convert from ImageToVideoInput to Fal API input format."""
    
    @staticmethod
    def validate_and_convert_image_to_video_input(data: dict) -> dict:
        """
        Validates the input data and converts it to Fal API input format.
        
        Args:
            data: The input data to validate and convert.
            
        Returns:
            dict: The converted input data for Fal API.
        """
        # Validate the input data
        input_model = ImageToVideoInput.model_validate(data)
        
        # Create FalInput instance with mapped values
        fal_input = FalInput(
            prompt=input_model.prompt,
            start_image_url=input_model.start_image,
            end_image_url=input_model.end_image,
            num_frames=input_model.number_of_frames,
            frames_per_second=input_model.frames_per_second,
            resolution=input_model.resolution,
            aspect_ratio=input_model.aspect_ratio,
            num_inference_steps=input_model.number_of_steps,
            guide_scale=input_model.guidance_scale,
            seed=input_model.seed,
            enable_prompt_expansion=input_model.prompt_enhancer,
            acceleration=input_model.acceleration,
        )
        
        # Convert to dict, excluding None values
        return fal_input.model_dump(exclude_none=True)    
