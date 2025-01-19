import json
from enum import Enum


class SubjectCode(Enum):
    MODERN_INDIAN_HISTORY = "MIH"
    HISTORY_ART_AND_CULTURE = "HAC"
    POLITY = "POL"
    INTERNATIONAL_RELATIONS = "IR"
    SECURITY = 'SEC'
    ECONOMICS = "ECO"
    SCIENCE_AND_TECH = "ST"
    ENVIRONMENT = "ENV"
    GEOGRAPHY = "GEO"
    MISCELLANEOUS = "MISC"


class PatternType(Enum):
    SINGLE_STATEMENT = "SINGLE"
    TWO_STATEMENT_CORRECT_OPTIONS = "TWO_CORR"
    TWO_STATEMENTS_ASSERTION_REASONING = "ASSERTION"
    MULTIPLE_STATEMENTS = "MULTI_STMT"
    MULTIPLE_OPTIONS_SELECT_CORRECT_ELIMINATION = "MULTI_ELIM"
    MULTIPLE_OPTIONS_SELECT_NUMBER_STYLE = "MULTI_NUM"
    MATCH_THE_PAIRS_CODE_STYLE = "MATCH_CODE"
    MATCH_THE_PAIRS_NUMBER_STYLE = "MATCH_NUM"
    MULTIPLE_DESCRIPTIONS_IDENTIFY_SUBJECT = "MULTI_DESC"


class QuestionDifficultyLevel(Enum):
    EASY = 'easy'
    MODERATE = 'moderate'
    DIFFICULT = 'difficult'


class PDFFileType(Enum):
    SCANNED = 'scanned'
    DIGITAL = 'digital'


def write_to_json(data, output_path):
    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def merge_json_lists(list1_path, list2_path, output_file_path):
    try:
        with open(list1_path, 'r') as f1:
            list1 = json.load(f1)
        with open(list2_path, 'r') as f2:
            list2 = json.load(f2)
        if not isinstance(list1, list):
            raise ValueError("First file does not contain a JSON list.")
        if not isinstance(list2, list):
            raise ValueError("Second file does not contain a JSON list.")
        merged_list = list1 + list2
        with open(output_file_path, 'w') as outfile:
            json.dump(merged_list, outfile, indent=4)
        print(f"Successfully merged {list1_path} and {list2_path} into {output_file_path}")
    except FileNotFoundError:
        print(f"Error: One or both input files not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Error: {e}")


def wrap_text_file(input_file, output_file, line_length=80):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.strip():
                words = line.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= line_length:
                        current_line += word + " "
                    else:
                        f_out.write(current_line.strip() + "\n")
                        current_line = word + " "
                if current_line:
                    f_out.write(current_line.strip() + "\n")
            else:
                f_out.write("\n")
