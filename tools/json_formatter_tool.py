import os
import json
import re
from RAW.RAW.tool import Tool
from llm.side_llm import side_llm

def process_text_with_agent(text: str) -> list:
    print("Processing full text with agent...")
    """
    Sends the entire text to the LLM and returns detected topics as a JSON array.
    """
    prompt = f'''
Given the following text:

"""{text}"""

Your task is to analyze this text and detect distinct topics present.

IMPORTANT: You MUST respond ONLY with a valid JSON array with NO additional text or explanations. Include the full content of each topic in the response, do not reduce the content or remove any details.

Carefully parse through each line of the text and determine which topic it belongs to.
If content appears to be misclassified or fragmented across the text, assign it to the correct topic.
Some lines of a particular topic may be intermixed with other topics - please identify and group them appropriately.

IMPORTANT: Make sure all strings are properly terminated with double quotes and all special characters within strings are properly escaped.

Your response should look exactly like this (with your actual topics and content):
[
    {{
        "Topic": "First Topic",
        "Content": "Content for first topic"
    }},
    {{
        "Topic": "Second Topic",
        "Content": "Content for second topic"
    }}
]
'''
    
    messages = [
        {"role": "system", "content": "You are an AI that extracts structured topic-wise information from text. Your response must be ONLY valid JSON with no other text."},
        {"role": "user", "content": prompt}
    ]
    
    # Call the LLM
    response = side_llm.execute(messages)
    print(f"Raw LLM response: {response}")

    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        # Attempt to fix common JSON formatting issues
        try:
            response = response.strip()
            if response.startswith("```json"):  # Remove markdown formatting
                response = response.replace("```json", "").replace("```", "")
            response = response.replace("\n", " ")  # Remove newlines
            response = response.replace("\t", " ")  # Remove tabs
            response = response.strip()
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON after cleanup: {e}")
            raise 

def convert_text_to_topic_json(file_path: str) -> str:
    """
    Reads the text file and processes the entire content using the agent.
    Creates a separate JSON file for each identified topic in a new folder.
    Returns the paths of the generated JSON files.
    """
    print("Converting text to topic-based JSON files...")
    # Read the extracted text file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()
    except Exception as e:
        return f"Error reading file: {e}"
    
    # Create a new folder to store the JSON files
    cwd = os.getcwd()
    folder_name = "topic_json_files"
    output_dir = os.path.join(cwd, folder_name)
    
    # Create the folder if it doesn't exist
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created new directory: {output_dir}")
    except Exception as e:
        return f"Error creating directory: {e}"
    
    # Process the entire text with the agent
    try:
        topic_results = process_text_with_agent(full_text)
    except Exception as e:
        return f"Error processing text: {e}"
    
    if not topic_results:
        return "Error: No topics were identified or there was an error processing the text. Check the logs for details."
    
    output_files = []

    # Write each topic's JSON object to a separate file in the new directory
    for topic_obj in topic_results:
        topic = topic_obj.get("Topic", "Unknown")
        content = topic_obj.get("Content", "")
        
        # Skip empty topics
        if not content.strip():
            continue
        
        topic_data = {"Topic": topic, "Content": content}
        
        # Create a safe file name by replacing spaces and special characters with underscores
        safe_filename = re.sub(r'[^\w\s-]', '', topic.replace(' ', '_'))
        filename = os.path.join(output_dir, f"{safe_filename}.json")
        print(f"filename: {filename}")
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(topic_data, f, indent=4, ensure_ascii=False)
            output_files.append(filename)
        except Exception as e:
            return f"Error writing JSON file for topic '{topic}': {e}"
    
    return f"JSON files created in '{folder_name}' folder: {', '.join([os.path.basename(f) for f in output_files])}"

json_formatter_tool = Tool(
    description="Converts a text file into multiple topic-based JSON files. Processes the entire text at once to identify topics and correctly assign content to each topic, even when content from different topics is intermixed. Creates a 'topic_json_files' folder in the current working directory to store the output JSON files.",
    name="json_formatter_tool",
    action=convert_text_to_topic_json,
    example="extracted_text.txt",
    test_payloads=[]
)