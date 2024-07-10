#!/bin/bash

# Arguments
input_xlsx_path="tutta_la_storia_eval_con_conversazione.xlsx"
local_image_dir="cambia_questa_riga_con_la_cartella_che_contiene_le_immagini"
output_xlsx_path="annotazioni_monika.xlsx"

# Install required Python packages
pip install pandas pillow openpyxl tk

# Run the Python script
python interfaccia_per_comparare.py "$input_xlsx_path" "$local_image_dir" "$output_xlsx_path"

