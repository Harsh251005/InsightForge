import yaml


def load_prompt(name: str) -> str:
    with open("config/prompts.yaml", "r") as file:
        prompts = yaml.safe_load(file)

    return prompts.get(name, "")