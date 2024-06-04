import os

class TextQueryEngine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text_data = self.load_text_data(file_path)
    
    def load_text_data(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Text file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def query(self, query_str):
        lines = self.text_data.split('\n')
        matching_lines = [line for line in lines if query_str.lower() in line.lower()]
        return '\n'.join(matching_lines) if matching_lines else "No matching lines found."
