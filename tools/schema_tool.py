import os
from RAW.RAW.tool import Tool
from llm.side_llm import side_llm

def convert_to_schema_md(file_path: str) -> str:
    """
    Reads a JSON file describing a database schema and uses an LLM to generate a Markdown file.
    The resulting Markdown will be formatted similar to the provided schema.md sample.
    """
    print("Converting JSON schema to Markdown documentation...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json_content = f.read()
    except Exception as e:
        return f"Error reading JSON file: {e}"
    
    # Define the prompt for the LLM
    prompt = f"""
You are an expert database documenter. Given the following JSON content that describes a database schema, generate a Markdown file that documents the schema.

The Markdown should follow this format:

# Database Schema Documentation

## Overview
Provide an overview of the database including its name, version, and description.

## Tables
For each table, list:
### <table_name>
*Description:* <table description>

Then create a Markdown table with the following columns:
| Column Name | Data Type | Constraints | Description |
Fill in the column details as provided in the JSON.

## Relationships
If any relationships are provided in the JSON, list them as bullet points.

## Last Updated
Include a hard-coded date "March 16, 2025".

Here is the JSON:
{json_content}
"""
    messages = [
        {"role": "system", "content": "You are an expert in converting JSON schema descriptions to formatted Markdown documentation."},
        {"role": "user", "content": prompt}
    ]
    
    # Call the LLM to get the Markdown output
    response = side_llm.execute(messages)
    
    # Write the LLM response to a Markdown file named 'schema.md'
    output_md = os.path.join(os.getcwd(), "schema.md")
    try:
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(response)
    except Exception as e:
        return f"Error writing Markdown file: {e}"
    
    return f"Markdown file 'schema.md' created successfully in {os.getcwd()}."

# Create a new tool instance
schema_tool = Tool(
    description="Uses an LLM to convert a JSON file describing a database schema into a formatted Markdown file ('schema.md').",
    name="llm_json_to_schema_md_tool",
    action=convert_to_schema_md,
    example="database_schema.json",
    test_payloads=[]
)
