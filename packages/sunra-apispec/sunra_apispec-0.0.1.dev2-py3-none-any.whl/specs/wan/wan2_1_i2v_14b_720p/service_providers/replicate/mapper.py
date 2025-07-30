from typing import Dict, Any
from ...input_schema import Image2VideoInput
from .schema import ReplicateInput


class Wan21I2V14b720PReplicateMapper:
    """Mapper class to convert from Image2VideoInput to Replicate API input format."""
    
    @staticmethod
    def toReplicateInput(input_model: Image2VideoInput) -> Dict[str, Any]:
        """
        Convert Image2VideoInput model to Replicate input format.
        
        Args:
            input_model: The Image2VideoInput model instance
            
        Returns:
            Dictionary compatible with Replicate API input format
        """
        # Map fast_mode from "On"/"Off" to Replicate's options
        fast_mode_mapping = {
            "Off": "Balanced",
            "On": "Fast"  # Map "On" to "Fast" as default acceleration level
        }
        
        # Create ReplicateInput instance with mapped values
        replicate_input = ReplicateInput(
            prompt=input_model.prompt,
            seed=input_model.seed,
            sample_steps=input_model.number_of_steps,
            sample_guide_scale=input_model.guidance_scale,
            aspect_ratio=input_model.aspect_ratio,
            num_frames=input_model.number_of_frames,
            frames_per_second=input_model.frames_per_second,
            fast_mode=fast_mode_mapping.get(input_model.fast_mode, "Balanced")
        )
        
        # Convert to dict, excluding None values
        return replicate_input.model_dump(exclude_none=True)
