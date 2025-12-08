# 📚 Study Notes Search Engine

A powerful web application that allows you to upload study notes in various formats (TXT, PDF, PPT, PPTX) and search through them like a personal Google for your study materials.

## ✨ Features

### Core Functionality
- **Multi-format Support**: Upload TXT, PDF, PPT, and PPTX files
- **Smart Search**: Intelligent full-text search with context
- **Highlighted Results**: Search terms are highlighted in yellow
- **Snippet Display**: Shows relevant text snippets around matches
- **Match Counter**: Displays total number of matches per file

### Advanced Features
- **Auto-Generated Summaries**: Automatic extractive summaries for each uploaded file
- **Keyword Cloud**: Visual display of most important terms with frequency counts
- **Search History**: Tracks and displays recent searches for quick re-use
- **Multiple Files**: Upload and search across multiple documents simultaneously
- **File Management**: View all uploaded files with summaries and delete option
- **Drag & Drop**: Easy drag-and-drop file upload interface

### User Experience
- Beautiful gradient UI design
- Responsive layout
- Real-time search with instant results
- Click keywords to search for them
- Click search history to repeat searches
- Context-aware snippets (shows surrounding text)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Download the Files
Create a new directory and save these files:
- `app.py` (main Flask application)
- `requirements.txt` (Python dependencies)
- Create a `templates` folder and save `index.html` inside it

### Step 2: Project Structure
```
study-notes-search/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── uploads/ (will be created automatically)
```

### Step 3: Install Dependencies
Open terminal/command prompt in your project directory and run:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Step 5: Open in Browser
Open your web browser and go to:
```
http://127.0.0.1:5000
```

## 📖 How to Use

### Uploading Files
1. Click "Choose File" or drag and drop a file onto the upload area
2. Supported formats: TXT, PDF, PPT, PPTX (max 16MB)
3. The file will be processed automatically
4. You'll see a success message with word count and summary

### Searching
1. Type your search query in the search box
2. Press Enter or click "Search"
3. Results show:
   - Filename with match count
   - Text snippets with highlighted search terms
   - Context around each match

### Using Keywords
- Click any keyword in the keyword cloud to search for it
- Keywords are ranked by frequency
- Useful for exploring important concepts

### Search History
- Your recent searches appear as clickable tags
- Click any tag to repeat that search
- Last 10 searches are remembered

### Managing Files
- View all uploaded files in the "Uploaded Files" section
- Each file shows its summary and word count
- Click the delete button to remove a file

## 🔧 Technical Details

### Text Extraction
- **TXT**: Direct file reading with UTF-8 encoding
- **PDF**: Uses `pdfplumber` (primary) and `PyPDF2` (fallback)
- **PPT/PPTX**: Extracts text from all slides and shapes

### Search Algorithm
1. Creates an inverted index for fast searching
2. Finds all occurrences of search terms
3. Extracts surrounding sentences for context
4. Highlights matches in yellow
5. Ranks results by match count

### Summary Generation
- Extractive approach (selects important sentences)
- Scores sentences by unique word count
- Returns top 3 sentences as summary

### Keyword Extraction
- Removes common stop words
- Counts word frequency
- Returns top 15 most frequent meaningful words

## 🎨 Customization

### Changing Port
Edit `app.py`, last line:
```python
app.run(debug=True, port=5000)  # Change port number here
```

### File Size Limit
Edit `app.py`, line 13:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Change to desired bytes
```

### Number of Snippets
Edit `app.py`, line 94:
```python
for match in unique_matches[:5]:  # Change 5 to show more/fewer snippets
```

### Keyword Count
Edit `app.py`, line 158:
```python
def get_keyword_frequency(text, top_n=15):  # Change 15 to desired count
```

## 🛠️ Troubleshooting

### "Module not found" error
```bash
pip install --upgrade -r requirements.txt
```

### PDF extraction fails
- Try a different PDF (some are scanned images)
- Install additional dependencies:
```bash
pip install pypdf pillow
```

### PowerPoint extraction fails
- Ensure file is not corrupted
- Try re-saving the file in PowerPoint

### Port already in use
- Change the port number in `app.py`
- Or kill the process using the port

## 📝 Example Queries

Good search queries:
- `"gradient descent"` - Find specific terms
- `"machine learning"` - Multi-word concepts
- `"definition"` - Find definitions
- `"chapter 3"` - Search by location
- `"algorithm"` - Technical terms

## 🔒 Privacy & Security

- Files are processed locally on your machine
- No data is sent to external servers
- Uploaded files are deleted after processing
- Notes are stored in memory only (lost when app closes)
- For persistent storage, modify the code to use a database

## 🚀 Future Enhancements

Potential improvements you could add:
- Persistent database storage (SQLite, PostgreSQL)
- User accounts and authentication
- Export search results to PDF
- Advanced filtering (by file, date, etc.)
- Synonym search and fuzzy matching
- Question answering with AI
- Mobile app version
- Cloud deployment

## 📄 License

Free to use and modify for educational purposes.

## 🤝 Contributing

Feel free to enhance this project! Some ideas:
- Add support for DOCX files
- Implement fuzzy search
- Add export functionality
- Improve summary algorithm
- Add more visualization options

## 💡 Tips for Best Results

1. **Upload multiple related files** for comprehensive searches
2. **Use specific terms** rather than general words
3. **Try variations** of terms if first search doesn't find matches
4. **Click keywords** to explore important concepts
5. **Review summaries** to understand file content quickly

## 📞 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Ensure Python version is 3.8+
3. Verify file formats are supported
4. Check file isn't corrupted
5. Review error messages in terminal

---

Happy studying! 📖✨