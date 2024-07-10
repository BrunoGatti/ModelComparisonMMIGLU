import pandas as pd
import sys
import re

def normalize_text(text):
    return ''.join(e for e in text.lower() if e.isalnum() or e.isspace())

def is_question(text):
    return text.strip().endswith('?')

def main(file_path):
    # Load the data
    data = pd.read_excel(file_path)

    # Normalize and recalculate perfect matches
    data['Recalculated Perfect match'] = data.apply(
        lambda row: 1 if normalize_text(row['Expected output']) == normalize_text(row['Model output']) else 0,
        axis=1
    )

    # Calculate the percentage of recalculated perfect matches
    recalculated_perfect_matches = data['Recalculated Perfect match'].sum()
    total_entries = len(data)
    percentage_recalculated_perfect_match = (recalculated_perfect_matches / total_entries) * 100

    # Calculate the percentage of times the model asked a question
    model_questions = data['Model output'].apply(is_question).sum()
    percentage_model_questions = (model_questions / total_entries) * 100

    # Calculate the percentage of times the expected output was a question and the model answered with "Posso eseguirlo"
    expected_questions_model_statements = data.apply(
        lambda row: 1 if is_question(row['Expected output']) and row['Model output'].strip().lower() in ['posso eseguirlo', 'posso eseguirlo.'] else 0,
        axis=1
    ).sum()
    percentage_expected_questions_model_statements = (expected_questions_model_statements / total_entries) * 100

    # Calculate the percentage of times the expected output was "Posso eseguirlo" and the model answered with a question
    expected_statements_model_questions = data.apply(
        lambda row: 1 if row['Expected output'].strip().lower() in ['posso eseguirlo', 'posso eseguirlo.'] and is_question(row['Model output']) else 0,
        axis=1
    ).sum()
    percentage_expected_statements_model_questions = (expected_statements_model_questions / total_entries) * 100

    # Print the results
    print(f"Percentage of recalculated perfect matches: {percentage_recalculated_perfect_match:.2f}%")
    print(f"Percentage of times the model asked a question: {percentage_model_questions:.2f}%")
    print(f"Percentage of times the expected output was a question and the model answered with 'Posso eseguirlo': {percentage_expected_questions_model_statements:.2f}%")
    print(f"Percentage of times the expected output was 'Posso eseguirlo' and the model answered with a question: {percentage_expected_statements_model_questions:.2f}%")

    # Save the updated DataFrame to a new Excel file
    output_file_path = 'updated_output.xlsx'  # Replace with the desired output path
    data.to_excel(output_file_path, index=False)
    print(f"Updated data saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_excel_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)

