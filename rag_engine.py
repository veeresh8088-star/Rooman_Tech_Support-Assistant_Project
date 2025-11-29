import os
from typing import List
try:
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
except Exception:
    OpenAIEmbeddings = None
    Chroma = None

def load_faqs(path='data/faqs.txt'):
    if not os.path.exists(path):
        return []
    raw = open(path,'r',encoding='utf-8').read().strip()
    blocks = [b.strip() for b in raw.split('\n\n') if b.strip()]
    items = []
    for b in blocks:
        lines = b.split('\n')
        if lines[0].startswith('Q:'):
            q = lines[0].replace('Q:','').strip()
        else:
            q = lines[0].strip()
        k = []
        a_lines = []
        for ln in lines[1:]:
            if ln.strip().startswith('K:'):
                k = [kw.strip().lower() for kw in ln.replace('K:','').split(',')]
            elif ln.strip().startswith('A:'):
                a_lines.append(ln.replace('A:','').strip())
            else:
                a_lines.append(ln.strip())
        a = '\n'.join(a_lines).strip()
        items.append({'q':q,'k':k,'a':a})
    return items

def keyword_match(user_input: str, items: List[dict], min_score: int=1):
    ui = user_input.lower()
    results = []
    for item in items:
        score = 0
        for kw in item.get('k',[]):
            if kw and kw in ui:
                score += 2
        if score >= min_score:
            results.append((score,item))
    results.sort(key=lambda x: x[0], reverse=True)
    return results

def ensure_vectorstore(faq_path='data/faqs.txt', persist_dir='vectorstore/chroma_db'):
    if OpenAIEmbeddings is None or Chroma is None:
        return False
    raw = open(faq_path,'r',encoding='utf-8').read()
    texts = [t.strip() for t in raw.split('\n\n') if t.strip()]
    emb = OpenAIEmbeddings()
    db = Chroma.from_texts(texts, emb, persist_directory=persist_dir)
    db.persist()
    return True

def semantic_search(query: str, top_k: int=3, persist_dir='vectorstore/chroma_db'):
    if OpenAIEmbeddings is None or Chroma is None:
        return []
    emb = OpenAIEmbeddings()
    db = Chroma(persist_directory=persist_dir, embedding_function=emb)
    docs = db.similarity_search(query, k=top_k)
    results = []
    for d in docs:
        if hasattr(d,'page_content'):
            results.append(d.page_content)
        elif isinstance(d, dict) and 'page_content' in d:
            results.append(d['page_content'])
        else:
            results.append(str(d))
    return results
