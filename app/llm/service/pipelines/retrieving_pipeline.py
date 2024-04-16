from app.llm.service.preprocessing.data_preprocessing import text_cleaning



def get_top_context(query, vectordb):
    query_cleaned = text_cleaning(query)
    context = vectordb.search_context(query_cleaned)
    return context