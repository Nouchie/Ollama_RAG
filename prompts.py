from llama_index.core import PromptTemplate

instruction_str = """\
    1. Convert the query to executable SQL code.
    2. The final line of code should be a SQL query string.
    3. The query should be a solution to the prompt.
    4. PRINT ONLY THE QUERY.
    5. Do not quote the query."""

new_prompt = PromptTemplate(
    """\
    You are working with a SQL database.
    The name of the table is `dictionary_table`.
    Follow these instructions:
    {instruction_str}
    Query: {query_str}

    Query: """
)

context = """Purpose: The primary role of this agent is to assist users by providing accurate 
            translation of English to Dagaare. The agent is to use the dictionary to find context-specific translations.
            It should know the different words, how they are used, and in what manner to translate sentences.
            The agent should look through the data and learn how Dagaare sentences are formed to get a better understanding of the translations."""

translation_prompt = PromptTemplate(
    """\
    {context}
    Translate the following phrase from English to Dagaare using the dictionary:
    Phrase: {query_str}

    Translation: """
)
