
def operation_chains_message(question: str, pre_text: str, post_text: str, table: str) ->str:
    
    operation_chains_message = f'''
    Here is the question:
    {question}
    Here is the text before the table:
    {pre_text}
    Here is the table containing the numerical data:
    {table}
    Here is the text after the table:
    {post_text}
    '''

    
    return operation_chains_message


def entity_extraction_message(operation_steps_json: str, pre_text: str, post_text: str, table: str) ->str:
    
    # entity_extractor_message = f'''
    # Here are the operation steps:
    # {operation_steps_json}
    # Here is the text before the table:
    # {pre_text}
    # Here is the table containing the numerical data:
    # {table}
    # Here is the text after the table:
    # {post_text}
    # '''
    
    entity_extractor_message = f'''
    Here are the operation steps:
    {operation_steps_json}

    Here is the table containing the numerical data:
    {table}

    '''
    
    return entity_extractor_message