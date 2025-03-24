from RAW.RAW import Agent
from typing import List
from RAW.RAW import Tool
from RAW.RAW import TextColor, BackgroundColor
from llm.file_formatting_llm import file_formatting_llm
from tools.pdf_extraction_tool import pdf_extractor_tool
from tools.json_formatter_tool import json_formatter_tool
from tools.markdown_formatter_tool import markdown_formatter_tool
from tools.schema_tool import schema_tool

def file_formatting_agent(tools: List[Tool]=[], subordinates: List[Agent]=[]):
    fileformatting =  Agent(
        llm=file_formatting_llm, 
        name="file_formatting_agent", 
        personality="smart and helpful", 
        role="Performs file formatting tasks such as extracting text from PDF files.", 
        tools=[pdf_extractor_tool, json_formatter_tool, markdown_formatter_tool, schema_tool], 
        textColor=TextColor.GREEN,
        backgroundColor=BackgroundColor.BLACK,
        exampleSession="""

        Question: I want to extract text from a PDF file

        Thought: I need to ask for the file path

        Follow Up: Please provide the file path

        Through: Now I have the file path, I should use the pdf_extractor_tool to extract the text

        Action: pdf_extractor_tool('example.pdf')
        PAUSE

        Observation: Ok I have the text extracted from the PDF file

        Answer: Here is the text extracted from the PDF file:

        Question: I want to convert the extracted text into a JSON file

        Thought: User asked me to convert the extracted text into a JSON file, so i should use the json_formatter_tool

        Action: json_formatter_tool('extracted_text.txt')
        PAUSE

        Observation: Ok I have the JSON file

        Answer: Here is the JSON file:

        Question: I want to convert the extracted text into a markdown file

        Thought: User asked me to convert the extracted text into a markdown file, so i should use the markdown_formatter_tool

        Action: markdown_formatter_tool('extracted_text.txt')
        PAUSE

        Observation: Ok I have the markdown file

        Answer: Here is the markdown file:

        Question: I want to make a markdown file for some database information 

        Though: I need to ask for the file path

        Follow Up: Please provide the file path

        Through: Now I have the file path, I should use the schema_tool to make a markdown file

        Action: schema_tool('database_information.json')
        PAUSE

        Observation: Ok I have the markdown file

        Answer: Here is the markdown file:
    """
    )

    return fileformatting
