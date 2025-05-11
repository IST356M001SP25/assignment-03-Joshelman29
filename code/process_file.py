'''
Next, write a streamlit to read ONE file of packaging information. 
You should output the parsed package and total package size for each package in the file.

Screenshot available as process_file.png
'''

import streamlit as st
import packaging
from io import StringIO
import json
import os

def process_packaging_file():
    st.title("Bulk Package Data Processor")
    
    uploaded_file = st.file_uploader(
        "Upload packaging data file:", 
        type=["txt"],
        help="Upload a text file with one package description per line"
    )
    
    if uploaded_file:
        # Process file data
        original_filename = uploaded_file.name
        output_filename = original_filename.replace(".txt", ".json")
        all_packages = []
        
        # Read file content
        file_content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        
        # Display processing header
        st.subheader("Package Processing Results")
        
        # Process each line
        for line in file_content.split("\n"):
            line = line.strip()
            if not line:
                continue
                
            try:
                parsed_pkg = packaging.parse_packaging(line)
                total_units = packaging.calc_total_units(parsed_pkg)
                unit_type = packaging.get_unit(parsed_pkg)
                all_packages.append(parsed_pkg)
                
                # Display package info in simple format
                st.info(f"{line} ➡️ Total Units: {total_units} {unit_type}")
                
            except Exception as e:
                st.error(f"Error processing: '{line}' - {str(e)}")
        
        # Save JSON output
        os.makedirs("./data", exist_ok=True)
        output_path = f"./data/{output_filename}"
        
        with open(output_path, "w") as f:
            json.dump(all_packages, f, indent=4)
        
        st.success(
            f"Processed {len(all_packages)} packages. " 
            f"Saved to {output_path}",
            icon="✅"
        )


process_packaging_file()