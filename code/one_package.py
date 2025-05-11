'''
Write a streamlit to input one string of package data. 
It should use the `packaging.py` module to parse the string 
and output the package info as it appears. 
Calculate the total package size and display that.

see one_package.png for a screenshot
'''


import streamlit as st
import packaging

def display_package_analysis():
    st.title("Package Processing Application")
    
    package_input = st.text_input("Enter packaging information string:")
    
    if package_input:
        analyzed_package = packaging.parse_packaging(package_input)
        total_quantity = packaging.calc_total_units(analyzed_package)
        measurement_unit = packaging.get_unit(analyzed_package)
        
        st.text("Package Composition Breakdown:")
        for component in analyzed_package:
            item_name = list(component.keys())[0]
            item_amount = list(component.values())[0]
            st.info(f"{item_name} ➡️ {item_amount}")
        
        st.success(f"Complete Package Quantity: {total_quantity} {measurement_unit}")


display_package_analysis()