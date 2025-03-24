import os
import re
from RAW.RAW.tool import Tool
from llm.side_llm import side_llm

def process_text_with_agent(text: str) -> list:
    print("Processing full text with agent...")
    prompt = f'''
    Given the following text:

    """{text}"""

    Your task is to analyze the text and extract distinct topics.

    For each topic, generate a properly formatted Markdown document with:
    - A title in H1 format (`# Topic Name`)
    - The relevant content properly structured in Markdown.

    IMPORTANT: Your response must be strictly formatted in Markdown. DO NOT return JSON or any other format. Just provide the properly formatted Markdown text. Include the full content of each topic in the response, do not reduce the content or remove any details. Do not return any additional text or explanations.
    '''
    
    messages = [
        {"role": "system", "content": "You are an AI that extracts structured topic-wise information from text. Your response must be ONLY valid JSON with no other text."},
        {"role": "user", "content": prompt}
    ]
    
    response = side_llm.execute(messages)
    return response

def convert_text_to_topic_markdown(file_path: str) -> str:
    print("Converting text to topic-based Markdown files...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
    cwd = os.getcwd()
    folder_name = "topic_md_files"
    output_dir = os.path.join(cwd, folder_name)
    
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created new directory: {output_dir}")
    except Exception as e:
        return f"Error creating directory: {e}"
    
    try:
        topic_results = process_text_with_agent(full_text)
    except Exception as e:
        return f"Error processing text: {e}"
    
    if not topic_results:
        return "Error: No topics were identified. Check the logs."
    
    output_files = []

    sections = re.split(r'(?m)^#\s(.+)$', topic_results)
    if len(sections) < 2:
        return "Error: No topics were identified."
    
    for i in range(1, len(sections), 2):
        topic = sections[i].strip()
        content = sections[i+1].strip() if i+1 < len(sections) else ""
        
        if not content:
            continue
        
        safe_filename = re.sub(r'[^\w\s-]', '', topic.replace(' ', '_'))
        filename = os.path.join(output_dir, f"{safe_filename}.md")
        
        markdown_content = f"# {topic}\n\n{content}\n"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            output_files.append(filename)
        except Exception as e:
            return f"Error writing Markdown file for topic '{topic}': {e}"
    
    return f"Markdown files created in '{folder_name}' folder: {', '.join([os.path.basename(f) for f in output_files])}"

markdown_formatter_tool = Tool(
    description="Converts a text file into multiple topic-based Markdown files. Creates a 'topic_md_files' folder in the current working directory to store the output Markdown files.",
    name="markdown_formatter_tool",
    action=convert_text_to_topic_markdown,
    example="extracted_text.txt",
    test_payloads=[]
)
