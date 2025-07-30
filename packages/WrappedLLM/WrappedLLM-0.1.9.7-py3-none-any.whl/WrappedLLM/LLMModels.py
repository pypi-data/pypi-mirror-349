from typing import Optional

def get_info(provider: Optional[str] = None):
    """
    Retrieves information about available LLM (Large Language Model) models.
    
    The `get_info` function returns a dictionary containing information about the available LLM models. If a `provider` parameter is provided, it will return information only for that provider. Otherwise, it will return information for all available providers.
    
    The returned dictionary has the following structure:
    {
        "provider_name": {
            "model_name": {
                "display_name": "Friendly model name",
                "api_name": "API-friendly model name",
                "description": "Description of the model",
                "image_upload": True/False (whether the model supports image upload)
            }
        }
    }
    """
        
    all_models_info = {
    "openai": {
        "gpt-3.5-turbo-0125": {
            "display_name": "GPT-3.5 Turbo",
            "api_name": "gpt3_5",
            "description": "Efficient and cost-effective model for various tasks.",
            "image_upload": False,
            "cost_per_1k_tokens": {
                "input": 0.0005,
                "output": 0.0015
            }
        },
        "gpt-4-turbo-2024-04-09": {
            "display_name": "GPT-4 Turbo",
            "api_name": "gpt4",
            "description": "Advanced model with improved reasoning and broader knowledge.",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.01,
                "output": 0.03
            }
        },
        "gpt-4o-2024-08-06": {
            "display_name": "GPT-4 Omni",
            "api_name": "gpt4_omni",
            "description": "Optimized GPT-4 model with enhanced performance.",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.0025,
                "output": 0.01
            }
        },
        "gpt-4o-mini-2024-07-18": {
            "display_name": "GPT-4 Omni Mini",
            "api_name": "gpt4_omni_mini",
            "description": "Compact version of GPT-4o optimized for faster responses and is the cheapest option.",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.00015,
                "output": 0.0006
            }
        },
        "o3-2025-04-16": {
            "display_name": "GPT o3",
            "api_name": "gpt_o3",
            "description": "Our most powerful reasoning model with leading performance on coding, math, science, and vision",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.01,
                "output": 0.04
            }
        },
        "o3-mini-2025-01-31": {
            "display_name": "GPT O3 Mini",
            "api_name": "gpt_o3_mini",
            "description": "Small cost-efficient reasoning model that’s optimized for coding, math, and science, and supports tools and Structured Outputs",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.0011,
                "output": 0.0044
            }
        },
        "gpt-4.1-2025-04-14": {
            "display_name": "GPT 4.1",
            "api_name": "gpt4_1",
            "description": "Smartest model for complex tasks",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.0020,
                "output": 0.0080
            }
        },
        "gpt-4.1-mini-2025-04-14": {
            "display_name": "GPT 4.1 Mini",
            "api_name": "gpt4_1_mini",
            "description": "Affordable model balancing speed and intelligence",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.0004,
                "output": 0.0016
            }
        },
        "gpt-4.1-nano-2025-04-14": {
            "display_name": "GPT 4.1 Nano",
            "api_name": "gpt4_1_nano",
            "description": "Fastest, most cost-effective model for low-latency tasks",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.0001,
                "output": 0.0004
            }
        },
        "o4-mini-2025-04-16": {
            "display_name": "GPT o4 Mini",
            "api_name": "gpt_o4_mini",
            "description": "Our faster, cost-efficient reasoning model delivering strong performance on math, coding and vision",
            "image_upload": True,
            "cost_per_1k_tokens": {
                "input": 0.0011,
                "output": 0.0044
            }
        },
        
    },
        "anthropic": {
            "claude-3-5-sonnet-20240620": {
                "display_name": "Claude 3.5 Sonnet",
                "api_name": "claude3_5_sonnet",
                "description": "Balanced model for general-purpose tasks.",
                "image_upload": True
            },
            "claude-3-opus-20240229": {
                "display_name": "Claude 3 Opus",
                "api_name": "claude3_opus",
                "description": "Most capable Claude model for complex tasks.",
                "image_upload": True
            },
            "claude-3-sonnet-20240229": {
                "display_name": "Claude 3 Sonnet",
                "api_name": "claude3_sonnet",
                "description": "Versatile model balancing performance and speed.",
                "image_upload": True
            },
            "claude-3-haiku-20240307": {
                "display_name": "Claude 3 Haiku",
                "api_name": "claude3_haiku",
                "description": "Fastest Claude model, ideal for quick responses.",
                "image_upload": True
            }
        },
        "google": {
            "gemini-1.5-flash-latest": {
                "display_name": "Gemini 1.5 Flash",
                "api_name": "gemini1_5_flash",
                "description": "Fast and efficient model for various applications.",
                "image_upload": False
            }
        }
    }
    
    if provider:
        return {provider: all_models_info.get(provider, {})}
    return all_models_info


# Original LLM_MODELS dictionary for backwards compatibility
LLM_MODELS = {
    "openai": {
        "gpt3_5": "gpt-3.5-turbo-0125",
        "gpt4": "gpt-4-turbo-2024-04-09",
        "gpt4_omni": "gpt-4o-2024-08-06",
        "gpt4_omni_mini": "gpt-4o-mini-2024-07-18",
        "gpt_o3": "o3-2025-04-16",
        "gpt_o3_mini": "o3-mini-2025-01-31",
        "gpt_o4_mini": "o4-mini-2025-04-16",
        "gpt4_1": "gpt-4.1-2025-04-14",
        "gpt4_1_mini": "gpt-4.1-mini-2025-04-14",
        "gpt4_1_nano": "gpt-4.1-nano-2025-04-14"
    },
    "anthropic": {
        "claude3_5_sonnet": "claude-3-5-sonnet-20240620",
        "claude3_opus": "claude-3-opus-20240229",
        "claude3_sonnet": "claude-3-sonnet-20240229",
        "claude3_haiku": "claude-3-haiku-20240307"
    },
    "google": {
        "gemini1_5_flash": "gemini-1.5-flash-latest"
    }
}
