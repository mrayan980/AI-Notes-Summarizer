import re
from collections import defaultdict

def search_in_text(text, query, context_chars=150):
    """
    Search for query in text and return results with context
    """
    results = []
    query_lower = query.lower()
    text_lower = text.lower()
    
    # Split text into lines for line number tracking
    lines = text.split('\n')
    
    # Track matches
    match_count = 0
    position = 0
    
    # Find all occurrences
    while True:
        pos = text_lower.find(query_lower, position)
        if pos == -1:
            break
        
        match_count += 1
        
        # Find which line this match is on
        line_num = text[:pos].count('\n') + 1
        
        # Get context around the match
        start = max(0, pos - context_chars)
        end = min(len(text), pos + len(query) + context_chars)
        
        snippet = text[start:end]
        
        # Add ellipsis if needed
        if start > 0:
            snippet = '...' + snippet
        if end < len(text):
            snippet = snippet + '...'
        
        # Highlight the query in the snippet
        highlighted_snippet = highlight_text(snippet, query)
        
        # Extract page/slide number if present
        page_num = extract_page_number(text, pos)
        
        results.append({
            'line_number': line_num,
            'page_number': page_num,
            'snippet': highlighted_snippet,
            'position': pos
        })
        
        position = pos + 1
    
    return {
        'matches': results,
        'count': match_count,
        'query': query
    }

def highlight_text(text, query):
    """
    Highlight query terms in text using <mark> tags
    """
    # Escape special regex characters in query
    escaped_query = re.escape(query)
    
    # Case-insensitive replacement with highlight
    pattern = re.compile(escaped_query, re.IGNORECASE)
    highlighted = pattern.sub(lambda m: f'<mark>{m.group(0)}</mark>', text)
    
    return highlighted

def extract_page_number(text, position):
    """
    Try to extract page/slide number near the position
    """
    # Look backwards for page/slide markers
    search_text = text[max(0, position - 500):position]
    
    # Look for patterns like "--- Page 5 ---" or "--- Slide 3 ---"
    page_match = re.findall(r'---\s*(?:Page|Slide)\s+(\d+)\s*---', search_text)
    
    if page_match:
        return int(page_match[-1])
    
    return None

def search_multiple_terms(text, queries):
    """
    Search for multiple terms and combine results
    """
    all_results = []
    
    for query in queries:
        results = search_in_text(text, query)
        all_results.append(results)
    
    return all_results

def fuzzy_search(text, query, max_distance=2):
    """
    Simple fuzzy search (allows small typos)
    """
    # This is a simplified version - for production, use a library like fuzzywuzzy
    words = text.split()
    matches = []
    
    query_lower = query.lower()
    
    for i, word in enumerate(words):
        word_lower = word.lower()
        
        # Check if query is in word or vice versa
        if query_lower in word_lower or word_lower in query_lower:
            matches.append({
                'word': word,
                'position': i,
                'context': ' '.join(words[max(0, i-5):i+6])
            })
    
    return matches

def get_word_frequency(text, top_n=20):
    """
    Get most frequent words in text
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Tokenize and count
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    word_freq = defaultdict(int)
    
    for word in words:
        if word not in stop_words:
            word_freq[word] += 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_words[:top_n]

def search_with_operators(text, query):
    """
    Search with boolean operators (AND, OR, NOT)
    """
    # Simple implementation of boolean search
    if ' AND ' in query.upper():
        terms = [t.strip() for t in re.split(r'\s+AND\s+', query, flags=re.IGNORECASE)]
        results = []
        for term in terms:
            term_results = search_in_text(text, term)
            results.append(term_results)
        return results
    
    elif ' OR ' in query.upper():
        terms = [t.strip() for t in re.split(r'\s+OR\s+', query, flags=re.IGNORECASE)]
        combined_results = []
        for term in terms:
            term_results = search_in_text(text, term)
            combined_results.extend(term_results['matches'])
        return {
            'matches': combined_results,
            'count': len(combined_results),
            'query': query
        }
    
    else:
        return search_in_text(text, query)