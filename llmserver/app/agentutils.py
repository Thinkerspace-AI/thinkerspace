import os
import json
from pathlib import Path

from langchain_core.runnables.utils import ConfigurableFieldMultiOption

# These prompts will not be loaded by load_agent_options
SPECIAL_PROMPTS = [
    "convener.json",
]

def load_agent_options() -> ConfigurableFieldMultiOption:
    prompts_dir = Path(__file__).resolve().parent / "prompts"
    options = {}

    for filename in os.listdir(prompts_dir):
        # Check if the file is a JSON file
        if filename in SPECIAL_PROMPTS or not filename.endswith('.json'):
            continue
            
        with open(prompts_dir / filename, 'r') as f:
            try:
                data = json.load(f)
                name = data.get('name')
                template = data.get('template')
                template += "\n{history}\n{human_input}"
                options.update({name: template})
                
            except json.JSONDecodeError:
                print(f"Error: {filename} is not a valid JSON file")
            except KeyError:
                print(f"Error: {filename} does not contain an 'input' field")
    
    return ConfigurableFieldMultiOption(
        id="agent",
        default="generic",
        options=options
    )