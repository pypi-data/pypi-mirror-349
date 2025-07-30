import os
from pydantic import BaseModel
from typing import List, Dict, Tuple, Union, Optional, Any
from .LLMInitialization import Initialize as ini
from .LLMModels import LLM_MODELS
from .GPTFunctions import GPTImage, format_response


class Output:
    """
    Provides methods for generating output from various large language models (LLMs).
    
    The `Output` class provides static methods for generating output from different LLM models, including GPT, Claude, and Gemini. Each method takes a prompt as input and returns the generated output.
    
    The `GPT` method uses the OpenAI GPT model to generate output, with options to specify the model, temperature, and maximum tokens. The `Claude` method uses the Anthropic Claude model, with similar options. The `Gemini` method uses the Gemini model, which does not have any additional options.
    
    All methods raise a `ValueError` if the provided model name is invalid or the temperature is out of the valid range.
    """
        
    @staticmethod
    def GPT(
        user_prompt, 
        system_prompt: Optional[str] = None, 
        model: str = "gpt-4o-mini-2024-07-18", 
        temperature: float = 0.15, 
        max_tokens: int = 1024, 
        response_format: Optional[BaseModel] = None, 
        output_option: str = 'cont_prt_det', 
        images: Optional[List[Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]]]] = None
    ):
        """
            Generates output using the OpenAI GPT language model.

            Args:
                user_prompt (str): The input prompt to generate output from.
                system_prompt (str, optional): The system prompt to provide context for the generation.
                model (str, optional): The name of the GPT model to use. Defaults to "gpt-4o-mini-2024-07-18".
                temperature (float, optional): The temperature value to use for generating output. Must be between 0 and 1. Defaults to 0.15.
                max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 1024.
                response_format (BaseModel, optional): The response format to use for the generated output.
                output_option (str, optional): The output option to use for the generated output. Defaults to 'cont_prt_det'.
                images (List[Union[str, os.PathLike, Tuple[Union[str, os.PathLike], str]]], optional): The images to include for generating output.

            Returns:
                GPTResponse: An object containing the generated output, token usage, and cost breakdown.

            Raises:
                ValueError: If the provided model name is invalid, the temperature is out of the valid range, or the output option is invalid.
        """

        # Initialize the ChatGPT client
        chatgpt = ini.get_chatgpt()
        
        # Validate the model name against available OpenAI models
        if model not in LLM_MODELS['openai'].values():
            raise ValueError(f"Invalid model name: {model}. Please use one of the following: {', '.join(LLM_MODELS['openai'].values())}")
        
        # Ensure temperature is within valid range
        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        
        # Define and validate output options
        valid_out_opts = ['cont', 'cont_prt_det', 'cont_prt_min', 'cont_cost', 'cont_cost_prt_det', 'cont_cost_prt_min']
        if output_option not in valid_out_opts:
            raise ValueError(f"Invalid out_opt. Please choose from: {', '.join(valid_out_opts)}")
        
        # Initialize messages list for the conversation
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Handle image inputs if provided
        if images:
            # Verify model supports image input (GPT-4 only)
            # print(model)
            if not any(model.startswith(prefix) for prefix in ["gpt-4o", "gpt-4-","gpt-4.1-","o4-mini-", "o3-2025-"]):
                raise ValueError("Image input is only supported forcertain reasoning and GPT-4 models.")
            
            content = []
            
            # Process and add each image to content
            for image_data in images:
                content.append(GPTImage.process(image_data))
            
            # Add the user's text prompt
            content.append({
            "type": "text",
            "text": user_prompt
            })    
            
            # Combine images and text into user message
            messages.append({
            "role": "user",
            "content": content
            })

        else:
            # Add text-only user prompt
            messages.append({"role": "user", "content": user_prompt})
        
        # Set up base completion arguments
        base_completion_args = {
            "model": model,
            "messages": messages,
            "max_completion_tokens": max_tokens
        }
        print(model)
        # Add additional arguments for non-o3 models
        if "o3" not in model and "o4" not in model:
            del base_completion_args['max_completion_tokens']
            additional_args = {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            completion_args = {**base_completion_args, **additional_args}
        else:
            completion_args = base_completion_args        
        
        # Generate response with specified format or default
        if response_format:
            completion_args["response_format"] = response_format
            response = chatgpt.beta.chat.completions.parse(**completion_args)
        else:
            # print(completion_args)
            response = chatgpt.chat.completions.create(**completion_args)
        
        # Extract content from response
        content = response.choices[0].message.content if not response_format else response.choices[0].message.parsed
        
        # Format and return the response according to specified output option
        return format_response(response, content, response_format, output_option, model)
        

    @staticmethod
    def Claude(user_prompt, system_prompt: Optional[str] = None, model: str = "claude-3-5-sonnet-20240620", temperature: float = 0, max_tokens: int = 2048):
        """
            Generates a response from the Anthropic Claude language model based on the provided user prompt and optional system prompt.
            
            Args:
                user_prompt (str): The prompt to be sent to the language model.
                system_prompt (Optional[str]): An optional system prompt to be used by the language model.
                model (str): The name of the language model to use. Must be one of the values in LLM_MODELS['anthropic'].
                temperature (float): The temperature parameter for the language model, which controls the randomness of the generated output. Must be between 0 and 1.
                max_tokens (int): The maximum number of tokens to generate in the response.
            
            Returns:
                str: The generated response from the language model.
        """   
        
        claude = ini.get_claude()
        
        if model not in LLM_MODELS['anthropic'].values():
            raise ValueError(f"Invalid model name: {model}. Please use one of the following: {', '.join(LLM_MODELS['anthropic'].values())}")
        
        if not 0 <= temperature <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        
        message = claude.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ],
                }
            ],
        )
        return message.content[0].text
    
    @staticmethod
    def Gemini(prompt):
        gemini = ini.get_gemini()
        
        return gemini.generate_content(prompt)