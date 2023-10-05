import re
import os
import markdown

class TaxonTraitTextSearch:

    def __init__(self,
                 keyword_taxon,
                 keyword_traits,
                 txt_input_dir=os.path.join('raw_data', 'txt_database')):
        self.keyword_taxon = [k.lower() for k in keyword_taxon]
        self.keyword_traits = [k.lower() for k in keyword_traits]
        self.keyword_taxon_regex = [
            re.compile(rf'\b{re.escape(k)}\b', re.IGNORECASE) for k in keyword_taxon
        ]
        self.keyword_traits_regex = [
            re.compile(rf'\b{re.escape(k)}\b', re.IGNORECASE) for k in keyword_traits
        ]
        self.txt_input_dir = txt_input_dir

    def search_paragraphs(self, paragraphs):
            results = []
            for paragraph in paragraphs:
                if any(regex.search(paragraph.lower()) for regex in self.keyword_taxon_regex):
                    if any(regex.search(paragraph.lower()) for regex in self.keyword_traits_regex):
                        # Highlight keywords
                        for regex in self.keyword_taxon_regex + self.keyword_traits_regex:
                            paragraph = regex.sub(lambda m: f"**{m.group(0)}**", paragraph)
                            # Convert the Markdown-formatted string to HTML
                        paragraph = markdown.markdown(paragraph)
                        results.append(paragraph)
            return results


    def search_through_txt(self):
            results = {}
            for file_name in os.listdir(self.txt_input_dir):
                if file_name.endswith('.txt'):
                    txt_file_path = os.path.join(self.txt_input_dir, file_name)
                    with open(txt_file_path, 'r') as f:
                        paragraphs = f.read().split('\n\n')  # Adjust as needed based on how you saved paragraphs
                        filtered_paragraphs = self.search_paragraphs(paragraphs)
                        if filtered_paragraphs:  # Only add entries for files where keywords were found
                            results[file_name] = filtered_paragraphs
            return results
