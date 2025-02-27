from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO, StringIO

class PDFTextExtractor:
    def extract_text(self,pdf_file: BytesIO) -> str:
    
        try:
            # Create resource manager
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()

            # Set parameters for analysis
            laparams = LAParams()

            # Create a text converter object
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)

            # Create a PDF interpreter object
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # Process each page
            for page in PDFPage.get_pages(pdf_file):
                interpreter.process_page(page)

            text = retstr.getvalue()

            # Cleanup
            device.close()
            retstr.close()

            return text.strip()

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")