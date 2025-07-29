import pytest
import os
from ebooklib import epub
from typing import List, Tuple
from epub_helper import get_toc, get_meta  

@pytest.fixture
def sample_epub(tmp_path):
    """Create a simple EPUB file for testing"""
    # Create EPUB book
    book = epub.EpubBook()
    book.set_title('Sample Book')
    book.set_language('en')
    
    # Create chapters
    c1 = epub.EpubHtml(title='Chapter 1', file_name='chap1.xhtml', content='<h1>Chapter 1</h1><p>Content</p>')
    c2 = epub.EpubHtml(title='Chapter 2', file_name='chap2.xhtml', content='<h1>Chapter 2</h1><p>Content</p>')
    c3 = epub.EpubHtml(title='Subchapter 2.1', file_name='chap2_1.xhtml', content='<h1>Subchapter 2.1</h1><p>Content</p>')
    
    # Add chapters to book
    book.add_item(c1)
    book.add_item(c2)
    book.add_item(c3)
    
    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create spine
    book.spine = ['nav', c1, c2, c3]
    
    # Add TOC
    book.toc = [(c1, []), (c2, [c3])]
    
    # Add required files
    book.add_item(epub.EpubItem(uid='style_nav', file_name='style/nav.css', media_type='text/css', content=''))
    
    # Set EPUB options
    epub_options = {
        'epub2_guide': True,
        'epub3_landmark': True,
        'epub3_pages': True,
        'landmark_title': 'Guide',
        'pages_title': 'Pages',
        'spine_direction': True,
        'package_direction': True,
        'navigation_direction': True
    }
    
    # Save EPUB file
    epub_path = os.path.join(tmp_path, 'test_book.epub')
    epub.write_epub(epub_path, book, epub_options)
    
    return epub_path

def test_get_toc_success(sample_epub):
    """Test successful TOC retrieval"""
    toc = get_toc(sample_epub)
    
    assert isinstance(toc, list)
    assert len(toc) == 3
    assert toc[0] == ('Chapter 1', 'chap1.xhtml')
    assert toc[1] == ('Chapter 2', 'chap2.xhtml')
    assert toc[2] == ('Subchapter 2.1', 'chap2_1.xhtml')

def test_get_toc_file_not_found():
    """Test case when file does not exist"""
    with pytest.raises(FileNotFoundError):
        get_toc('/nonexistent/path/book.epub')

def test_get_toc_invalid_file(tmp_path):
    """Test invalid EPUB file"""
    # Create a non-EPUB file
    invalid_path = os.path.join(tmp_path, 'not_an_epub.txt')
    with open(invalid_path, 'w') as f:
        f.write('This is not an EPUB file')
    
    with pytest.raises(Exception, match="Failed to parse EPUB file"):
        get_toc(invalid_path)

def test_get_toc_empty_toc(tmp_path):
    """Test EPUB file without TOC"""
    # Create EPUB without TOC
    book = epub.EpubBook()
    book.set_title('Empty TOC Book')
    epub_path = os.path.join(tmp_path, 'empty_toc.epub')
    epub.write_epub(epub_path, book, {"ignore_ncx": True})
    
    with pytest.raises(Exception, match="Failed to parse EPUB file"):
        get_toc(epub_path)

@pytest.fixture
def sample_epub_with_meta(tmp_path):
    """Create a test EPUB file with metadata"""
    book = epub.EpubBook()
    
    # Add metadata
    book.set_identifier('123456789')
    book.set_title('Sample Book Title')
    book.add_author('Author One')
    book.add_author('Author Two')
    book.set_language('en')
    book.add_metadata('DC', 'date', '2023-01-01')
    book.add_metadata('DC', 'publisher', 'Test Publisher')
    book.add_metadata('DC', 'description', 'This is a test book description')
    book.add_metadata('DC', 'subject', 'Fiction')
    book.add_metadata('DC', 'subject', 'Science')
    
    # Add a chapter
    chapter = epub.EpubHtml(title='Chapter 1', file_name='chap1.xhtml', content='<h1>Chapter 1</h1>')
    book.add_item(chapter)
    
    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Create spine
    book.spine = ['nav', chapter]
    
    # Add TOC
    book.toc = [(chapter, [])]
    
    # Add required files
    book.add_item(epub.EpubItem(uid='style_nav', file_name='style/nav.css', media_type='text/css', content=''))
    
    # Set EPUB options
    epub_options = {
        'epub2_guide': True,
        'epub3_landmark': True,
        'epub3_pages': True,
        'landmark_title': 'Guide',
        'pages_title': 'Pages',
        'spine_direction': True,
        'package_direction': True,
        'navigation_direction': True
    }
    
    # Save file
    epub_path = os.path.join(tmp_path, 'test_meta.epub')
    epub.write_epub(epub_path, book, epub_options)
    
    return epub_path

def test_get_meta_success(sample_epub_with_meta):
    """Test successful metadata extraction"""
    meta = get_meta(sample_epub_with_meta)
    
    assert isinstance(meta, dict)
    assert meta['title'] == 'Sample Book Title'
    assert meta['identifier'] == '123456789'
    assert meta['language'] == 'en'
    assert meta['date'] == '2023-01-01'
    assert meta['publisher'] == 'Test Publisher'
    assert meta['description'] == 'This is a test book description'
    assert set(meta['creator']) == {'Author One', 'Author Two'}
    assert set(meta['subject']) == {'Fiction', 'Science'}

def test_get_meta_minimal_epub(tmp_path):
    """Test EPUB file with minimal metadata"""
    book = epub.EpubBook()
    book.set_identifier('minimal123')
    book.set_title('Minimal Book')
    
    # Add a chapter to make the file valid
    chapter = epub.EpubHtml(title='Chapter 1', file_name='chap1.xhtml')
    chapter.content = '<h1>Chapter 1</h1>'
    book.add_item(chapter)
    
    # Add navigation files
    nav = epub.EpubNav()
    book.add_item(nav)
    ncx = epub.EpubNcx()
    book.add_item(ncx)
    
    # Add to spine
    book.spine = ['nav', chapter]
    
    # Define TOC
    book.toc = [(chapter, [])]
    
    # Set EPUB options
    epub_options = {
        'epub2_guide': True,
        'epub3_landmark': True,
        'epub3_pages': True,
        'landmark_title': 'Guide',
        'pages_title': 'Pages',
        'spine_direction': True,
        'package_direction': True,
        'navigation_direction': True,
        'ignore_ncx': True
    }
    
    epub_path = os.path.join(tmp_path, 'minimal.epub')
    epub.write_epub(epub_path, book, epub_options)
    
    meta = get_meta(epub_path)
    
    assert meta['title'] == 'Minimal Book'
    assert meta['identifier'] == 'minimal123'
    assert 'language' not in meta  # Language field should not exist if not set
    assert 'creator' not in meta   # Creator field should not exist if not set

def test_get_meta_file_not_found():
    """Test case when file does not exist"""
    with pytest.raises(FileNotFoundError):
        get_meta('/nonexistent/path/book.epub')

def test_get_meta_invalid_file(tmp_path):
    """Test invalid EPUB file"""
    invalid_path = os.path.join(tmp_path, 'not_an_epub.txt')
    with open(invalid_path, 'w') as f:
        f.write('This is not an EPUB file')
    
    with pytest.raises(Exception, match="Failed to parse EPUB file"):
        get_meta(invalid_path)