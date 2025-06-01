def load_prompt_template(file_path='prompts/base_prompt.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()