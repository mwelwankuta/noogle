from typing import Dict, List
from dictionary import joining_words, question_words
from database import conn

db = conn.cursor()

def question_controller(args: Dict):
    query = args.get("q")
    results = []

    if len(query) == 0 or query is None:
        return []

    question = parse_question(query)

    for word in question.split(' '):
        wild_card_search = f"%{word}%"
        result = db.execute("""
        SELECT 
            meta.*, GROUP_CONCAT(titles.title, '+|+')
                AS titles 
            FROM meta LEFT JOIN titles 
                ON titles.meta_id = meta.id
            WHERE (meta.title != 'Main Page' AND meta.description != 'Main Page')
            AND 
                meta.description
                LIKE ? OR meta.title LIKE ? OR titles.title LIKE ? 
            GROUP BY
                meta.id;
        """, (wild_card_search, wild_card_search, wild_card_search, ))

        for row in result.fetchall():
            search_query_result = {
                "search_id": row[0],
                "search_title": row[1],
                "search_description": row[2],
                "titles": parse_title(row[4]),
            }
            results.append(search_query_result)
    
    kinda_ranked_search_results = sorted(results, key=lambda result: len(result["titles"]))
    return {"count": len(results), "optimal_search_query": question,"results": kinda_ranked_search_results,}

def parse_title(title: str) -> List[str]:
    if title is not None:
        titles = title.split("+|+")
        return titles
    return []

def parse_question(text: str):
    parsed_question = set()
    words = text.split(' ')
    for word in words:
        if is_question(word) == False and is_joining_word(word) == False:
            parsed_question.add(word)
    return " ".join(list(parsed_question))

def is_question(text:str):
    if text in question_words:
        return True
    return False

def is_joining_word(text:str):
    if text in joining_words:
        return True
    return False
