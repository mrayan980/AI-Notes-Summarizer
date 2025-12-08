import re
from collections import Counter, defaultdict
import string

def generate_summary(text, num_sentences=15, min_sentence_length=20):
    """
    Generate a summary using extractive summarization
    Uses sentence scoring based on word frequency and position
    """
    # Clean and prepare text
    sentences = split_into_sentences(text)
    
    if len(sentences) <= num_sentences:
        return {
            'text': text,
            'formatted': format_summary_output(text),
            'bullet_points': sentences
        }
    
    # Calculate word frequencies
    word_freq = calculate_word_frequency(text)
    
    # Score sentences
    sentence_scores = score_sentences(sentences, word_freq)
    
    # Get top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    
    # Sort by original order
    summary_sentences = sorted(top_sentences, key=lambda x: sentences.index(x[0]))
    
    # Extract just the sentences
    summary_text = ' '.join([s[0] for s in summary_sentences])
    
    # Format output
    formatted = format_summary_output(summary_text)
    
    return {
        'text': summary_text,
        'formatted': formatted,
        'bullet_points': [s[0] for s in summary_sentences]
    }

def split_into_sentences(text):
    """
    Split text into sentences
    """
    # Split on period, exclamation, question mark followed by space/newline
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Clean and filter
    cleaned = []
    for sent in sentences:
        sent = sent.strip()
        if len(sent) > 15 and not sent.startswith('---'):  # Skip page markers
            cleaned.append(sent)
    
    return cleaned

def calculate_word_frequency(text):
    """
    Calculate word frequency scores
    """
    # Remove stop words
    stop_words = get_stop_words()
    
    # Tokenize
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Count words (excluding stop words)
    word_count = Counter([w for w in words if w not in stop_words])
    
    # Normalize frequencies
    max_freq = max(word_count.values()) if word_count else 1
    word_freq = {word: freq / max_freq for word, freq in word_count.items()}
    
    return word_freq

def score_sentences(sentences, word_freq):
    """
    Score sentences based on word frequencies and other factors
    """
    sentence_scores = {}
    
    for i, sentence in enumerate(sentences):
        score = 0
        words = re.findall(r'\b[a-zA-Z]{3,}\b', sentence.lower())
        
        # Base score from word frequencies
        for word in words:
            if word in word_freq:
                score += word_freq[word]
        
        # Bonus for sentences near the beginning (introduction)
        if i < len(sentences) * 0.2:
            score *= 1.3
        
        # Bonus for sentences with important markers
        if any(marker in sentence.lower() for marker in ['important', 'key', 'definition', 'theorem', 'formula', 'conclusion', 'summary']):
            score *= 1.4
        
        # Bonus for sentences with numbers (likely formulas/data)
        if re.search(r'\d+', sentence):
            score *= 1.2
        
        # Penalty for very short sentences
        if len(words) < 5:
            score *= 0.5
        
        # Penalty for very long sentences
        if len(words) > 40:
            score *= 0.8
        
        sentence_scores[sentence] = score
    
    return sentence_scores

def extract_keywords(text, top_n=20):
    """
    Extract important keywords from text
    """
    stop_words = get_stop_words()
    
    # Tokenize
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Count words
    word_count = Counter([w for w in words if w not in stop_words])
    
    # Extract keywords with frequency > 1
    keywords = [word for word, count in word_count.most_common(top_n * 2) if count > 1]
    
    return keywords[:top_n]

def extract_definitions(text):
    """
    Extract potential definitions from text
    """
    definitions = []
    
    # Patterns for definitions
    patterns = [
        r'(.+?)\s+is\s+defined\s+as\s+(.+?)(?:\.|$)',
        r'(.+?)\s+means\s+(.+?)(?:\.|$)',
        r'(.+?):\s+(.+?)(?:\.|$)',
        r'Definition:\s+(.+?)(?:\.|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple) and len(match) >= 2:
                term = match[0].strip()
                definition = match[1].strip()
                if len(term) < 50 and len(definition) < 200:
                    definitions.append(f"{term}: {definition}")
            elif isinstance(match, str):
                definitions.append(match.strip())
    
    return definitions[:10]

def extract_formulas(text):
    """
    Extract mathematical formulas or equations
    """
    formulas = []
    
    # Look for lines with equals signs, math symbols
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Check if line contains math-like content
        if ('=' in line or '+' in line or '*' in line or '/' in line) and len(line) < 100:
            # Check if it has numbers or variables
            if re.search(r'[a-zA-Z]\s*[=+\-*/]\s*', line) or re.search(r'\d+\s*[=+\-*/]', line):
                formulas.append(line)
    
    return formulas[:15]

def extract_key_points(text):
    """
    Extract bullet points or numbered lists
    """
    key_points = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Check for bullet points or numbered lists
        if re.match(r'^[\•\-\*\d+\.]\s+', line) or re.match(r'^\d+\.\s+', line):
            key_points.append(line)
    
    return key_points[:20]

def format_summary_output(text):
    """
    Format summary into organized sections
    """
    sentences = split_into_sentences(text)
    
    # Group sentences into logical sections
    output = []
    output.append("📚 STUDY NOTES SUMMARY\n")
    output.append("=" * 50 + "\n\n")
    
    # Add sentences as bullet points
    output.append("KEY POINTS:\n")
    for i, sentence in enumerate(sentences, 1):
        output.append(f"{i}. {sentence}\n\n")
    
    return ''.join(output)

def generate_detailed_notes(text):
    """
    Generate comprehensive study notes
    """
    notes = {}
    
    # Extract different components
    notes['keywords'] = extract_keywords(text, 25)
    notes['definitions'] = extract_definitions(text)
    notes['formulas'] = extract_formulas(text)
    notes['key_points'] = extract_key_points(text)
    notes['summary'] = generate_summary(text, num_sentences=10)
    
    return notes

def get_stop_words():
    """
    Return common stop words
    """
    return {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them',
        'their', 'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all',
        'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        'just', 'also', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'then', 'once'
    }

def chunk_text(text, chunk_size=1000):
    """
    Split text into chunks of roughly equal size
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks