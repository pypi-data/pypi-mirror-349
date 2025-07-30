


from typing import List, Dict, Tuple, Union, Optional, Any, Literal
from pathlib import Path
import os
import imghdr
import base64
from dataclasses import dataclass
from .LLMModels import LLM_MODELS, get_info

class GPTImage:
    """
    A class for processing and preparing images for use with OpenAI's GPT-4 Vision models.
    
    This class provides methods to handle various image input formats (file paths, base64 strings),
    validate images, and prepare them in the format required by OpenAI's API with appropriate
    detail levels for optimizing token usage and analysis quality.
    
    Attributes:
        SUPPORTED_FORMATS (List[str]): List of supported image formats ('png', 'jpeg', 'jpg')
        DETAIL_LEVELS (List[str]): Valid detail levels for image processing ('auto', 'low', 'high')
        MAX_FILE_SIZE (int): Maximum allowed file size in bytes (20MB)
    
    Usage Examples:
        # Process a single image with default detail level
        image = GPTImage.process("path/to/image.jpg")
        
        # Process an image with specific detail level
        image = GPTImage.process("path/to/image.jpg", detail="high")
        
        # Process multiple images with different detail levels
        images = GPTImage.process_batch([
            ("path/to/image1.jpg", "high"),
            "path/to/image2.jpg",  # Uses default detail level
            base64_encoded_image
        ])
    """
    
    SUPPORTED_FORMATS = ['png', 'jpeg', 'jpg']
    DETAIL_LEVELS = ['auto', 'low', 'high']
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB
    
    @classmethod
    def process(cls, 
                image_data: Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]], 
                detail: Literal['auto', 'low', 'high'] = 'auto') -> Dict:
        """
        Process a single image for use with GPT-4 Vision models.
        
        Args:
            image_data: The image to process, which can be:
                - A file path (str or PathLike)
                - A base64-encoded string
                - A tuple of (image_source, detail_level)
            detail: The detail level to use for the image analysis.
                - 'low': Fixed 85 tokens, 512px resolution, faster but less detailed
                - 'high': More tokens, up to 2048x2048px, better for text and details
                - 'auto': Automatically selects between low/high based on image content
        
        Returns:
            Dict containing processed image data in the format required by OpenAI's API:
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/{format};base64,{content}",
                    "detail": detail_level
                }
            }
            
        Raises:
            ValueError: If the image file doesn't exist, has an unsupported format,
                       exceeds the maximum file size, or if the base64 string is invalid.
        """
        # Handle tuple input with explicit detail level
        if isinstance(image_data, tuple):
            img_source, detail = image_data
        else:
            img_source = image_data
            
        # Validate detail level
        if detail not in cls.DETAIL_LEVELS:
            raise ValueError(f"Detail level must be one of {cls.DETAIL_LEVELS}")
            
        # Process based on input type
        if isinstance(img_source, (str, os.PathLike)) and not cls._is_base64(img_source):
            return cls._process_file_path(img_source, detail)
        elif isinstance(img_source, str):
            return cls._process_base64(img_source, detail)
        else:
            raise ValueError("Image data must be a file path, base64 string, or tuple")
    
    @classmethod
    def process_batch(cls, 
                     images: List[Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]]]) -> List[Dict]:
        """
        Process multiple images for use with GPT-4 Vision models.
        
        Args:
            images: A list of images to process, where each item can be:
                - A file path (str or PathLike)
                - A base64-encoded string
                - A tuple of (image_source, detail_level)
        
        Returns:
            List[Dict]: A list of processed image data dictionaries
            
        Raises:
            ValueError: If any image processing fails
        """
        processed_images = []
        for img in images:
            processed_images.append(cls.process(img))
        return processed_images
    
    @classmethod
    def _process_file_path(cls, path: Union[str, os.PathLike], detail: str) -> Dict:
        """
        Process an image from a file path.
        
        Args:
            path: Path to the image file
            detail: Detail level for the image
            
        Returns:
            Dict: Processed image data
            
        Raises:
            ValueError: If the file doesn't exist, has an unsupported format, or exceeds size limit
        """
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Image file does not exist: {path}")
            
        # Check file size
        file_size = path.stat().st_size
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"Image file exceeds maximum size of 20MB: {file_size / (1024 * 1024):.2f}MB")
            
        # Validate format
        img_format = imghdr.what(path)
        if img_format not in cls.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {img_format}. Must be one of {cls.SUPPORTED_FORMATS}")
            
        # Read and encode file
        with open(path, "rb") as img_file:
            image_content = base64.b64encode(img_file.read()).decode('utf-8')
        
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{img_format};base64,{image_content}",
                "detail": detail
            }
        }
    
    @classmethod
    def _process_base64(cls, base64_str: str, detail: str) -> Dict:
        """
        Process a base64-encoded image string.
        
        Args:
            base64_str: Base64-encoded image string
            detail: Detail level for the image
            
        Returns:
            Dict: Processed image data
            
        Raises:
            ValueError: If the base64 string is invalid
        """
        try:
            # Handle data URI scheme
            if base64_str.startswith('data:image/'):
                # Extract format and content from data URI
                header, content = base64_str.split(',', 1)
                img_format = header.split('/')[1].split(';')[0]
                
                # Validate format
                if img_format not in cls.SUPPORTED_FORMATS:
                    raise ValueError(f"Unsupported image format: {img_format}. Must be one of {cls.SUPPORTED_FORMATS}")
                
                return {
                    "type": "image_url",
                    "image_url": {
                        "url": base64_str,
                        "detail": detail
                    }
                }
            else:
                # Verify raw base64 string
                base64.b64decode(base64_str)
                
                # Use PNG as default format for raw base64
                return {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_str}",
                        "detail": detail
                    }
                }
        except Exception as e:
            raise ValueError(f"Invalid base64 string provided for image: {str(e)}")
    
    @staticmethod
    def _is_base64(s: str) -> bool:
        """
        Check if a string is base64 encoded.
        
        Args:
            s: String to check
            
        Returns:
            bool: True if the string is base64 encoded, False otherwise
        """
        if not isinstance(s, str):
            return False
            
        # Check if it's a data URI
        if s.startswith('data:image/'):
            return True
            
        # Check if it's a raw base64 string
        try:
            base64.b64decode(s)
            return True
        except:
            return False
    
    @staticmethod
    def estimate_token_cost(
        image_dimensions: Tuple[int, int], 
        detail_level: Literal['low', 'high', 'auto'] = 'auto'
    ) -> Dict[str, int]:
        """
        Estimate the token cost for processing an image with GPT-4 Vision.
        
        Args:
            image_dimensions: Tuple of (width, height) in pixels
            detail_level: The detail level to use for the image
            
        Returns:
            Dict containing estimated token usage:
            {
                'tokens': int,  # Estimated total tokens
                'tiles': int,   # Number of 512px tiles (high detail only)
            }
        """
        width, height = image_dimensions
        
        # For low detail, always 85 tokens
        if detail_level == 'low':
            return {'tokens': 85, 'tiles': 0}
            
        # For auto detail, determine based on image size
        if detail_level == 'auto':
            # Simple heuristic: use high detail for images larger than 1024x1024
            if width > 1024 or height > 1024:
                detail_level = 'high'
            else:
                detail_level = 'low'
                return {'tokens': 85, 'tiles': 0}
        
        # For high detail
        # Scale the shortest side to 768px
        if width < height:
            scaled_width = 768
            scaled_height = int((height / width) * 768)
        else:
            scaled_height = 768
            scaled_width = int((width / height) * 768)
            
        # Cap at 2048px
        scaled_width = min(scaled_width, 2048)
        scaled_height = min(scaled_height, 2048)
        
        # Calculate number of 512px tiles
        tiles_x = (scaled_width + 511) // 512  # Ceiling division
        tiles_y = (scaled_height + 511) // 512
        total_tiles = tiles_x * tiles_y
        
        # Calculate tokens: 85 for initial pass + 170 per tile
        total_tokens = 85 + (170 * total_tiles)
        
        return {
            'tokens': total_tokens,
            'tiles': total_tiles
        }


@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cached_tokens: Optional[int] = None
    non_cached_tokens: Optional[int] = None
    reasoning_tokens: Optional[int] = None

@dataclass
class CostBreakdown:
    input_cost: float
    output_cost: float
    total_cost: float
    cached_cost: Optional[float] = None
    non_cached_cost: Optional[float] = None
    reasoning_cost: Optional[float] = None

class GPTResponse:
    """
        Represents a response from a GPT language model, capturing content, token usage, and cost details.
        
        Provides convenient properties and methods to access and summarize response metadata, including
        total tokens used, total cost, and a detailed breakdown of token and cost information.
        
        Attributes:
            content: The response content, which can be a string or another output object.
            token_usage: Detailed token usage statistics for the response.
            cost_breakdown: Comprehensive cost breakdown for the API call.
    """
        
    def __init__(self, content: Any, token_usage: TokenUsage, cost_breakdown: CostBreakdown):
        self.content = content
        self.token_usage = token_usage
        self.cost_breakdown = cost_breakdown

    @property
    def total_tokens(self) -> int:
        return self.token_usage.total_tokens

    @property
    def total_cost(self) -> float:
        return self.cost_breakdown.total_cost

    def __str__(self) -> str:
        
        if isinstance(self.content, str):
            return f"GPTResponse(content={self.content[:50]}..., total_tokens={self.total_tokens}, total_cost=${self.total_cost:.6f})"

        else:
            return f"GPTResponse(content=OutputObject..., total_tokens={self.total_tokens}, total_cost=${self.total_cost:.6f})"

    def __repr__(self) -> str:
        return self.__str__()

    def detailed_summary(self) -> str:
        cached_tokens = str(self.token_usage.cached_tokens) if self.token_usage.cached_tokens is not None else "N/A"
        non_cached_tokens = str(self.token_usage.non_cached_tokens) if self.token_usage.non_cached_tokens is not None else "N/A"
        reasoning_tokens = str(self.token_usage.reasoning_tokens) if self.token_usage.reasoning_tokens is not None else "N/A"
        cached_cost = f"${self.cost_breakdown.cached_cost:.6f}" if self.cost_breakdown.cached_cost is not None else "N/A"
        non_cached_cost = f"${self.cost_breakdown.non_cached_cost:.6f}" if self.cost_breakdown.non_cached_cost is not None else "N/A"
        return f"""
GPT Response Summary:
---------------------
Note: Reasoning Tokens are a subset of Completion Tokens. Please only consider Total Cost for the final cost.

Token Usage:
  Prompt tokens:     {self.token_usage.prompt_tokens}
  Completion tokens: {self.token_usage.completion_tokens}
  Total tokens:      {self.token_usage.total_tokens}
  Cached tokens:     {cached_tokens}
  Non-cached tokens: {non_cached_tokens}
  Reasoning tokens:  {reasoning_tokens}
  
Cost Breakdown:
  Input cost:        ${self.cost_breakdown.input_cost:.6f}
  Output cost:       ${self.cost_breakdown.output_cost:.6f}
  Total cost:        ${self.cost_breakdown.total_cost:.6f}
  Cached cost:       {cached_cost}
  Non-cached cost:   {non_cached_cost}
  Reasoning cost:    ${self.cost_breakdown.reasoning_cost:.6f}
"""



def format_response(response, content, response_format, output_option, model):
    """
    Formats the response from an LLM based on the specified output option.
    
    Args:
        response: The raw response object from the LLM.
        content: The extracted content from the response.
        response_format: Optional BaseModel for structured responses.
        output_option (str): The desired output format option.
        model (str): The name of the LLM model used.
        
    Returns:
        Union[str, GPTResponse]: The formatted response according to the output_option.
        
    Raises:
        ValueError: If the output option is invalid.
    """
    valid_out_opts = ['cont', 'cont_prt_det', 'cont_prt_min', 'cont_cost', 'cont_cost_prt_det', 'cont_cost_prt_min']
    if output_option not in valid_out_opts:
        raise ValueError(f"Invalid output_option. Please choose from: {', '.join(valid_out_opts)}")
    
    # Extract token usage information
    if hasattr(response.usage, 'completion_tokens_details') and hasattr(response.usage.completion_tokens_details, "audio_tokens"):
        cached_tokens = response.usage.prompt_tokens_details.cached_tokens
        reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens
    else:
        try:
            cached_tokens = response.usage.prompt_tokens_details.cached_tokens if hasattr(response.usage, 'prompt_tokens_details') else None
            reasoning_tokens = response.usage.completion_tokens_details.reasoning_tokens if hasattr(response.usage, 'completion_tokens_details') else None
        except:
            cached_tokens = response.usage.prompt_tokens_details.get('cached_tokens', 0) if hasattr(response.usage, 'prompt_tokens_details') else None 
            reasoning_tokens = response.usage.completion_tokens_details.get("reasoning_tokens", 0) if hasattr(response.usage, 'completion_tokens_details') else None
    
    token_usage = TokenUsage(
        prompt_tokens=response.usage.prompt_tokens,
        completion_tokens=response.usage.completion_tokens,
        total_tokens=response.usage.total_tokens,
        cached_tokens=cached_tokens,
        non_cached_tokens=response.usage.prompt_tokens - cached_tokens if cached_tokens is not None else None,
        reasoning_tokens=reasoning_tokens
    )

    # Calculate cost breakdown
    model_info = get_info("openai").get("openai").get(model)
    input_cost_rate = model_info["cost_per_1k_tokens"]["input"]
    output_cost_rate = model_info["cost_per_1k_tokens"]["output"]

    # Determine cached token cost ratio based on model
    # For GPT-4.1 models, cached tokens cost 1/4 of input tokens
    # For other models, cached tokens cost 1/2 of input tokens
    cached_cost_ratio = 0.25 if any(model_type in model.lower() for model_type in ["gpt-4.1", "gpt-o3", "o4-mini"]) else 0.5
    
    cached_cost = (token_usage.cached_tokens / 1000) * (input_cost_rate * cached_cost_ratio) if token_usage.cached_tokens is not None else None
    non_cached_cost = (token_usage.non_cached_tokens / 1000) * input_cost_rate if token_usage.non_cached_tokens is not None else None
    input_cost = cached_cost + non_cached_cost if cached_cost is not None and non_cached_cost is not None else (response.usage.prompt_tokens / 1000) * input_cost_rate
    output_cost = (token_usage.completion_tokens / 1000) * output_cost_rate
    reasoning_cost = (token_usage.reasoning_tokens / 1000) * output_cost_rate if token_usage.reasoning_tokens is not None else 0
    total_cost = input_cost + output_cost

    cost_breakdown = CostBreakdown(
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=total_cost,
        cached_cost=cached_cost,
        non_cached_cost=non_cached_cost,
        reasoning_cost=reasoning_cost
    )

    gpt_response = GPTResponse(content, token_usage, cost_breakdown)
    
    # Return based on output option
    if output_option == 'cont':
        return content
    
    if output_option in ['cont_cost_prt_det', 'cont_prt_det']:
        print(gpt_response.detailed_summary())
        return gpt_response if 'cost' in output_option else content
    
    elif output_option in ['cont_cost_prt_min', 'cont_prt_min']:
        print(f"\nTotal tokens: {gpt_response.total_tokens}")
        print(f"Total cost:   ${gpt_response.total_cost:.6f}")
        return gpt_response if 'cost' in output_option else content
    
    # Default case for 'cont_cost'
    return gpt_response

