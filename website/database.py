import pdfplumber
import os
import csv

INSTANCES_DIR = os.path.join('instances')
TXT_OUTPUT_DIR = os.path.join(INSTANCES_DIR, 'txt_database')
TSV_PATH = os.path.join(INSTANCES_DIR, 'main_database.tsv')


class Database:
    def __init__(self, pdf_from_user, txt_output_dir = TXT_OUTPUT_DIR, tsv_path= TSV_PATH):
        self.pdf_from_user = pdf_from_user
        self.txt_output_dir = txt_output_dir
        self.tsv_path = tsv_path
        self.file_name = os.path.basename(self.pdf_from_user).split('.pdf')[0] + '.txt'

    def extract_paragraphs_from_pdf(self):
        paragraphs = []
        with pdfplumber.open(self.pdf_from_user) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:  # Check if text is not None
                    for block in text.split('\n\n'):
                        paragraphs.append({
                            "text": block,
                            "page_number": page_number,
                        })
        return paragraphs

    def save_to_txt(self, paragraphs):
        txt_file_path = os.path.join(self.txt_output_dir, self.file_name)
        print(f"Saving to: {txt_file_path}")
        os.makedirs(self.txt_output_dir, exist_ok=True)  # Create output directory if not exists
        with open(txt_file_path, 'w') as f:
            for paragraph in paragraphs:
                f.write(f"Page {paragraph['page_number']}:\n{paragraph['text']}\n\n")


    def add_to_tsv(self, data):
        os.makedirs(os.path.dirname(self.tsv_path), exist_ok=True)  # Create dir if not exists
        print(f"Adding to TSV: {self.tsv_path}")
        print(f"Data: {data}")
        if not all(data):  # Validate that data is not empty or None
            raise ValueError("Data row contains empty or None values.")
        try:
            with open(self.tsv_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(data)
        except Exception as e:
            print(f"Error writing to TSV: {e}")



# Example usage
db = Database('../raw_data/test_pdf.pdf')
# paragraphs = db.extract_paragraphs_from_pdf()
# db.save_to_txt(paragraphs)
# Add to database:
data_row = [db.file_name, 'Sample Article', 'http://example.com', '2023', 'Author Name', 'Journal Name']
db.add_to_tsv(data_row)
