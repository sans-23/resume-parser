import pdfplumber # type: ignore
from io import BytesIO

class PDFTextExtractor:
    def extract_text(self, pdf_file: BytesIO) -> str:
        """
        Extracts text from a PDF file using pdfplumber.
        
        Args:
            pdf_file (BytesIO): A BytesIO object containing the PDF data.
            
        Returns:
            str: The extracted text from the PDF.
            
        Raises:
            Exception: If an error occurs during extraction.
        """
        try:
            # Reset the BytesIO object to the beginning
            pdf_file.seek(0)
            
            # Open the PDF with pdfplumber
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text.strip()
        
        except Exception as e:
            raise pdfplumber.exceptions.PDFSyntaxError(f"Error extracting text with pdfplumber: {str(e)}")