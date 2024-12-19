import unittest
from utilities.PromptTemplates import operation_chains_message, entity_extraction_message

def test_operation_chains_message():
    question = "What is 2 + 2?"
    pre_text = "This is a math problem."
    post_text = "Please solve the above question."
    table = "2 + 2 = ?"

    expected_output = f'''
    Here is the question:
    {question}
    Here is the text before the table:
    {pre_text}
    Here is the table containing the numerical data:
    {table}
    Here is the text after the table:
    {post_text}
    '''
    
    result = operation_chains_message(question, pre_text, post_text, table)
    assert expected_output == result
    
def test_entity_extraction_message():
    operation_steps_json = "[operation]"
    pre_text_op = "This is a math problem."
    post_text_op = "Please solve the above question."
    table_op = "2 + 2 = ?"

    entity_expected = f'''
    Here are the operation steps:
    {operation_steps_json}
    Here is the text before the table:
    {pre_text_op}
    Here is the table containing the numerical data:
    {table_op}
    Here is the text after the table:
    {post_text_op}
    '''
    
    result_op = entity_extraction_message(operation_steps_json, pre_text_op, post_text_op, table_op)
    assert entity_expected == result_op