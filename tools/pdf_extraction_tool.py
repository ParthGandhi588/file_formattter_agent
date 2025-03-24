from RAW.RAW.tool import Tool
import fitz  # PyMuPDF
import os


def extract_text_from_pdf(file_path: str, password: str = None, header_height: int = 70, footer_height: int = 70, use_ocr: bool = True) -> str:
    """
    Extracts text from a PDF file.
    If the PDF is encrypted, it uses the provided password.
    """
    print("Extracting text from PDF file...")
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        return f"Error opening file: {e}"
    
    if doc.is_encrypted:
        if password:
            if not doc.authenticate(password):
                doc.close()
                return "Error: Incorrect password provided for encrypted PDF."
        else:
            doc.close()
            return "Error: PDF is encrypted. Please provide a password."
    
    full_text = ""
    for page in doc:
        page_rect = page.rect
        body_rect = fitz.Rect(page_rect.x0, page_rect.y0 + header_height, page_rect.x1, page_rect.y1 - footer_height)
        text = page.get_text(clip=body_rect)
        full_text += text + "\n\n"
    doc.close()

    # Store extracted text in the same working directory
    temp_file_path = os.path.join(os.getcwd(), "extracted_text.txt")
    with open(temp_file_path, "w", encoding="utf-8") as temp_file:
        temp_file.write(full_text)
    
    return f"Extracted text saved to: {temp_file_path}"


pdf_extractor_tool = Tool(
    description="Extracts text from a PDF file.",
    name="pdf_extractor_tool",
    action=extract_text_from_pdf,
    example=" C:/Office_Work/Hexylon/File_Formatting_retry/sample.pdf ",
    test_payloads=[]
)