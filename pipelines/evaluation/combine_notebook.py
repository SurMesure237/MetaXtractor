#!/usr/bin/env python3
"""
Script to combine all notebook sections into the final improved evaluation notebook
"""

import json
import os

def load_json_sections(filepath):
    """Load sections from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_final_notebook():
    """Combine all sections into final notebook"""
    
    # Load base notebook
    with open('NER_Model_vs_SOMEF_Evaluation_Enhanced_Improved.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Load additional sections
    sections_2 = load_json_sections('notebook_sections_2.json')
    sections_3 = load_json_sections('notebook_sections_3.json')
    final_sections = load_json_sections('notebook_final_sections.json')
    export_sections = load_json_sections('notebook_export_sections.json')
    
    # Add all sections to notebook
    all_sections = [sections_2, sections_3, final_sections, export_sections]
    
    for section_file in all_sections:
        for key, cell in section_file.items():
            if isinstance(cell, dict) and 'cell_type' in cell:
                notebook['cells'].append(cell)
    
    # Save final notebook
    with open('NER_Model_vs_SOMEF_Evaluation_Complete.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print("✅ Created complete evaluation notebook: NER_Model_vs_SOMEF_Evaluation_Complete.ipynb")

if __name__ == "__main__":
    create_final_notebook()