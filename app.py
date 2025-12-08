from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename  
from utils.extraction import extract_text_from_file
from utils.search_utils import search_in_text, highlight_text
from utils.summarizer import generate_summary, extract_keywords
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'ppt', 'pptx', 'txt'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from file
        try:
            extracted_text = extract_text_from_file(filepath)
            
            # Store in session
            session['filename'] = filename
            session['text'] = extracted_text
            session['filepath'] = filepath
            
            flash(f'Successfully uploaded and processed: {filename}', 'success')
            return redirect(url_for('search_page'))
        
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    else:
        flash('Invalid file type. Please upload PDF, PPT, PPTX, or TXT files.', 'error')
        return redirect(url_for('index'))

@app.route('/search')
def search_page():
    if 'text' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('index'))
    
    return render_template('search.html', filename=session.get('filename', 'Unknown'))

@app.route('/search_results', methods=['POST'])
def search_results():
    if 'text' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('index'))
    
    query = request.form.get('query', '').strip()
    
    if not query:
        flash('Please enter a search query', 'warning')
        return redirect(url_for('search_page'))
    
    # Add to recent searches
    if 'recent_searches' not in session:
        session['recent_searches'] = []
    
    if query not in session['recent_searches']:
        session['recent_searches'].insert(0, query)
        session['recent_searches'] = session['recent_searches'][:5]  # Keep last 5
        session.modified = True
    
    # Perform search
    text = session['text']
    results = search_in_text(text, query)
    
    return render_template('results.html', 
                         query=query, 
                         results=results, 
                         filename=session.get('filename', 'Unknown'),
                         recent_searches=session.get('recent_searches', []))

@app.route('/summarize')
def summarize_page():
    if 'text' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('index'))
    
    text = session['text']
    filename = session.get('filename', 'Unknown')
    
    # Generate summary
    summary = generate_summary(text)
    keywords = extract_keywords(text)
    
    # Calculate stats
    word_count = len(text.split())
    char_count = len(text)
    line_count = len(text.split('\n'))
    
    stats = {
        'word_count': word_count,
        'char_count': char_count,
        'line_count': line_count,
        'compression_ratio': round((len(summary['text']) / word_count * 100), 1) if word_count > 0 else 0
    }
    
    return render_template('summarize.html',
                         filename=filename,
                         summary=summary,
                         keywords=keywords,
                         stats=stats)

@app.route('/download_summary')
def download_summary():
    if 'text' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('index'))
    
    from flask import Response
    
    text = session['text']
    filename = session.get('filename', 'Unknown')
    summary = generate_summary(text)
    keywords = extract_keywords(text)
    
    # Create downloadable text
    download_text = f"""STUDY NOTES SUMMARY
{'='*50}
Original File: {filename}

KEYWORDS:
{', '.join(keywords[:20])}

{'='*50}
SUMMARY:

{summary['formatted']}

{'='*50}
Generated by Study Notes Search Engine
"""
    
    return Response(
        download_text,
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment;filename=summary_{filename}.txt'}
    )

@app.route('/clear')
def clear_session():
    # Clean up uploaded file
    if 'filepath' in session:
        try:
            os.remove(session['filepath'])
        except:
            pass
    
    session.clear()
    flash('Session cleared. Upload a new file to start.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)