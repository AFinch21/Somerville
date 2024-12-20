import tiktoken
from logger.Logger import get_logger

logger = get_logger()

def count_tokens(model, input_text):
    try:
        # Retrieve the appropriate tokenizer for the given model
        encoding = tiktoken.get_encoding(model)
    except KeyError:
        # Default to 'cl100k_base' tokenizer for unknown models
        logger.error("Unrecognised encoding model")
        encoding = tiktoken.get_encoding("cl100k_base")

    # Encode the text and calculate the number of tokens
    tokenized_output = encoding.encode(input_text)
    num_tokens = len(tokenized_output)

    return num_tokens