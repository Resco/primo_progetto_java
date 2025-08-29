#!/usr/bin/env python3
"""
Blog Post Processor for Tilde.club Website
Processes .txt files from txt/ directory and converts them to HTML posts
"""

import os
import re
import shutil
from datetime import datetime
import glob
from bs4 import BeautifulSoup

def parse_markdown(text):
    """Convert basic markdown to HTML"""
    # Headers
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    
    # Bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    
    # Lists
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(\n<li>.+?</li>\n)+', r'<ul>\g<0></ul>', text, flags=re.DOTALL)
    
    # Numbered lists
    text = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(\n<li>.+?</li>\n)+', r'<ol>\g<0></ol>', text, flags=re.DOTALL)
    
    # Paragraphs
    text = re.sub(r'\n\n', r'</p>\n<p>', text)
    text = '<p>' + text + '</p>'
    
    # Clean up empty paragraphs
    text = re.sub(r'<p></p>', '', text)
    
    return text

def extract_title_and_date(content):
    """Extract title and date from post content"""
    lines = content.split('\n')
    title = "Untitled Post"
    date = datetime.now().strftime("%Y-%m-%d")
    
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    for line in lines:
        if '*' in line and any(month in line for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
            date_match = re.search(r'\*([^*]+)\*', line)
            if date_match:
                date_str = date_match.group(1).strip()
                # Convert date format to YYYY-MM-DD
                try:
                    date_obj = datetime.strptime(date_str, "%B %d, %Y")
                    date = date_obj.strftime("%Y-%m-%d")
                except:
                    pass
            break
    
    return title, date

def build_post_html(filename, content):
    """Build HTML for a single post"""
    title, date = extract_title_and_date(content)
    
    # Convert markdown to HTML
    html_content = parse_markdown(content)
    
    # Remove title and date from content to avoid duplication
    # Remove the first h1 (title)
    html_content = re.sub(r'<h1>.*?</h1>', '', html_content, count=1)
    # Remove the first em tag that contains the date
    html_content = re.sub(r'<em>.*?</em>', '', html_content, count=1)
    # Clean up any empty paragraphs
    html_content = re.sub(r'<p></p>', '', html_content)
    
    # Percorso assoluto del template rispetto allo script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'post-template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders
    html = template.replace('POST_TITLE', title)
    html = html.replace('POST_DATE', date)
    html = html.replace('POST_CONTENT', html_content)
    
    return html, title, date

def update_index_html(title, date, html_filename):
    """Add new blog entry to index.html"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Find the blog list
    blog_list = soup.find('div', class_='blog-list')
    if not blog_list:
        print("Error: Could not find blog-list in index.html")
        return False
    
    # Create new blog entry
    new_entry = soup.new_tag('div', attrs={'class': 'blog-entry'})
    
    # Date span
    date_span = soup.new_tag('span', attrs={'class': 'date'})
    date_span.string = date
    new_entry.append(date_span)
    
    # Separator
    separator = soup.new_tag('span', attrs={'class': 'separator'})
    separator.string = '~'
    new_entry.append(separator)
    
    # Link (pointing to posts directory)
    link = soup.new_tag('a', href=f"posts/{html_filename}")
    link.string = title
    new_entry.append(link)
    
    # Insert at the beginning of the blog list
    blog_list.insert(0, new_entry)
    
    # Write updated index.html with custom formatting for blog entries
    with open(index_path, 'w', encoding='utf-8') as f:
        # Get the prettified HTML
        html_content = soup.prettify()
        
        # Custom formatting for blog entries: each entry on one line
        # Find blog entries and format them
        lines = html_content.split('\n')
        formatted_lines = []
        in_blog_entry = False
        entry_buffer = []
        
        for line in lines:
            if '<div class="blog-entry">' in line:
                in_blog_entry = True
                entry_buffer = [line.strip()]
            elif in_blog_entry:
                entry_buffer.append(line.strip())
                if '</div>' in line:
                    # End of blog entry, format it on one line
                    entry_line = ' '.join(entry_buffer)
                    formatted_lines.append(entry_line)
                    in_blog_entry = False
                    entry_buffer = []
            else:
                formatted_lines.append(line)
        
        f.write('\n'.join(formatted_lines))
    
    return True

def main():
    """Main function to process all posts"""
    # Percorsi relativi alla posizione dello script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_dir = os.path.join(base_dir, 'txt')
    posts_dir = os.path.join(base_dir, 'posts')
    done_dir = os.path.join(txt_dir, 'done')
    
    if not os.path.exists(txt_dir):
        print(f"TXT directory '{txt_dir}' not found!")
        return
    
    # Get all .txt files (excluding done directory)
    txt_files = [f for f in glob.glob(os.path.join(txt_dir, '*.txt')) 
                 if 'done' not in f]
    
    if not txt_files:
        print("No .txt files found in txt directory!")
        return
    
    print(f"Found {len(txt_files)} posts to process...")
    
    for txt_file in txt_files:
        print(f"Processing {txt_file}...")
        
        # Read content
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Build HTML
        html_content, title, date = build_post_html(txt_file, content)
        
        # Create HTML filename
        base_name = os.path.splitext(os.path.basename(txt_file))[0]
        html_file = f"{base_name}.html"
        
        # Write HTML file in posts directory
        html_file_path = os.path.join(posts_dir, html_file)
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created {html_file}")
        
        # Update index.html
        if update_index_html(title, date, html_file):
            print(f"Updated index.html with new entry")
        else:
            print(f"Failed to update index.html")
        
        # Move file to done directory
        done_file = os.path.join(done_dir, os.path.basename(txt_file))
        shutil.move(txt_file, done_file)
        print(f"Moved {txt_file} to {done_file}")
        
        print(f"✅ Completed processing {txt_file}")
        print()
    
    print("All posts processed successfully!")

if __name__ == "__main__":
    main() 