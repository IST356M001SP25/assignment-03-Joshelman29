'''
In this final program, you will re-write your `process_file.py` 
to keep track of the number of files and total number of lines 
that have been processed.

For each file you read, you only need to output the 
summary information eg. "X packages written to file.json".

Screenshot available as process_files.png
'''

import streamlit as st
import packaging
from io import StringIO
import json
import os

def process_package_files():
    st.title("Package File Batch Processor")
    
    # Initialize session state for tracking
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = {
            'file_summaries': [],
            'cumulative_lines': 0,
            'files_processed': 0
        }
    
    # File upload interface
    uploaded_data = st.file_uploader(
        "Select package data file:", 
        type=["txt"],
        help="Text file with one package description per line"
    )
    
    if uploaded_data:
        # Process file data
        source_filename = uploaded_data.name
        output_filename = source_filename.replace(".txt", ".json")
        package_collection = []
        
        # Read and process file content
        file_contents = StringIO(uploaded_data.getvalue().decode("utf-8")).read()
        
        for entry in file_contents.split("\n"):
            entry = entry.strip()
            if entry:
                try:
                    parsed_entry = packaging.parse_packaging(entry)
                    package_collection.append(parsed_entry)
                except Exception as e:
                    st.warning(f"Skipped invalid entry: {entry} - {str(e)}")
        
        # Save processed data
        os.makedirs("./data", exist_ok=True)
        output_path = f"./data/{output_filename}"
        
        with open(output_path, "w") as output_file:
            json.dump(package_collection, output_file, indent=4)
        
        # Update processing statistics
        processed_count = len(package_collection)
        current_summary = f"{processed_count} packages saved to {output_filename}"
        
        st.session_state.processing_history['file_summaries'].append(current_summary)
        st.session_state.processing_history['files_processed'] += 1
        st.session_state.processing_history['cumulative_lines'] += processed_count
        
        # Display processing results
        st.subheader("Processing Summary")
        for summary in st.session_state.processing_history['file_summaries']:
            st.info(summary, icon="📦")
        
        st.success(
            f"Total: {st.session_state.processing_history['files_processed']} "
            f"files processed | {st.session_state.processing_history['cumulative_lines']} "
            "total packages processed"
        )


process_package_files()