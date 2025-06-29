#!/usr/bin/env python3
"""
Script to clean notebook metadata and remove problematic widget information
that causes GitHub rendering issues.
"""

import json
import sys
from pathlib import Path

def clean_notebook(notebook_path):
    """Remove widget metadata that causes GitHub rendering issues."""
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Clean global metadata
    if 'metadata' in notebook:
        # Remove widget state that might be causing issues
        if 'widgets' in notebook['metadata']:
            print("Removing widgets metadata from notebook metadata...")
            del notebook['metadata']['widgets']
        
        # Clean other problematic metadata
        problematic_keys = ['colab', 'kernelspec', 'language_info']
        for key in problematic_keys:
            if key in notebook['metadata']:
                print(f"Cleaning {key} from metadata...")
                if key == 'colab':
                    # Keep only essential colab metadata
                    if 'base_uri' in notebook['metadata'][key]:
                        notebook['metadata'][key] = {
                            'name': notebook['metadata'][key].get('name', 'Python 3')
                        }
                    else:
                        del notebook['metadata'][key]
    
    # Clean cell metadata and outputs
    if 'cells' in notebook:
        for cell in notebook['cells']:
            # Clean cell metadata
            if 'metadata' in cell:
                # Remove widget-related metadata from cells
                keys_to_remove = ['colab', 'widgets']
                for key in keys_to_remove:
                    if key in cell['metadata']:
                        print(f"Removing {key} from cell metadata...")
                        del cell['metadata'][key]
            
            # Clean cell outputs that might contain widget references
            if 'outputs' in cell:
                cleaned_outputs = []
                for output in cell['outputs']:
                    # Remove widget view outputs
                    if 'data' in output:
                        if 'application/vnd.jupyter.widget-view+json' in output['data']:
                            print("Removing widget view from cell output...")
                            del output['data']['application/vnd.jupyter.widget-view+json']
                        
                        # Keep output if it still has other data
                        if output['data']:
                            cleaned_outputs.append(output)
                    else:
                        cleaned_outputs.append(output)
                
                cell['outputs'] = cleaned_outputs
    
    # Create backup
    backup_path = notebook_path.with_suffix('.ipynb.backup')
    print(f"Creating backup at: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(json.load(open(notebook_path, 'r', encoding='utf-8')), f, indent=2)
    
    # Write cleaned notebook
    print(f"Writing cleaned notebook to: {notebook_path}")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print("Notebook cleaning completed!")

if __name__ == "__main__":
    notebook_path = Path("d:/my work/repositories/Vector-Databases-ChromaDB/Chroma_vectordb.ipynb")
    
    if not notebook_path.exists():
        print(f"Notebook not found: {notebook_path}")
        sys.exit(1)
    
    clean_notebook(notebook_path)
