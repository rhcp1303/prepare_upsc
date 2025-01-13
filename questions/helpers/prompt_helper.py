prompt_for_getting_explanation = """
    Give me the correct option of the above upsc prelims multiple choice question and also the explanation of the 
    correct answer by giving description about each named entity and important keywords in the question as well as 
    about the options when the options contain named entity or important keywords in the json format with two fields
    {"correct_option": correct option out of the four given ones,"explanation": detailed explanation}
    Below are some examples showing a question, explanation, and answer format:
**Example:**
**Prompt:** 
18. Which one of the following National Parks lies completely in the temperate alpine zone?
(a) Manas National Park
(b) Namdapha National Park
(c) Neora Valley National Park
(d) Valley of Flowers National Park

                **Response:**
correct_option: (d)
explanation: description about each of the national parks
"""


# question = ("create 10 upsc style mcqs with 4 options each  from 'parliament' topic, where"
    #             "one question should be of match the following pair type with the corresponding pairs jumbled up,"
    #             " one question should be of 2 statements type and requiring evaluation of it with four options,"
    #             "one question should be of single statement question based on factual recall with four options,"
    #             "one multiple statements and requiring the correct ones,"
    #             "one with few option statements/objects that need to be selected as per the question statement,"
    #             "make the questions so as to demand high factual recall,conceptual clarity, analytical skills,recall chronology,"
    #             "remember facts and data,application based and interdisciplinary in content "
    #             " avoid vague, unclear and obvious statements in the question and"
    #             "curate options so as to demand elimination techniques, identification, and remembering accurate concepts,data and facts,"
    #             "and set moderate to high difficulty by giving lot of distractors by not giving obvious distant options to the actual answer,"
    #             "also demand facts like literary source names, personality names, chronology"
    #             )

#     question = '''
#    1. In the context of global oil prices, "Brent crude oil" is frequently referred to in the news. What does this term imply?
# 1. It is a major classification of crude oil.
# 2. It is sourced from North Sea.
# 3. It does not contain sulphur.
# Which of the statements given above is/are correct?
# (a) 2 only
# (b) 1 and 2 only
# (c) 1 and 3 only
# (d) 1, 2 and 3
#
# give me correct answer and also the explanation and description of each options"
#     '''