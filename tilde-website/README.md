# Tilde.club Website

A minimal, text-focused website designed for the tilde.club community.

## Features

- **Minimal Design**: Clean, typography-focused layout
- **Responsive**: Works on desktop and mobile devices
- **Dark Mode Support**: Automatically adapts to user's system preferences
- **Fast Loading**: No external dependencies, pure HTML/CSS
- **Accessible**: Semantic HTML and keyboard navigation support

## Structure

```
tilde-website/
├── index.html              # Main page
├── style.css               # Stylesheet
├── post-template.html      # Template for blog posts
├── process_posts.py        # Script to process .txt files
├── txt/                    # Directory for new .txt files
│   ├── done/               # Processed files go here
│   └── 2025-01-20-new-post.txt
├── 2025-01-15-first-post.html    # Generated HTML post
├── 2025-01-10-minimal-design.html # Generated HTML post
└── README.md               # This file
```

## Customization

### Personal Information
Edit `index.html` to update:
- resco in the title and header
- About section content
- Projects list
- Contact information

### Blog Posts
The blog system works with simple `.txt` files:

1. **Create new posts**: Add `.txt` files to the `txt/` directory
2. **Format**: Use markdown-style formatting:
   ```
   # Post Title
   
   *Date*
   
   Your content here...
   ```
3. **Process posts**: Run `python process_posts.py` to:
   - Convert `.txt` to HTML posts
   - Add entries to the blog list in `index.html`
   - Move processed files to `txt/done/`
4. **Automatic workflow**: The script handles everything automatically

### Styling
Modify `style.css` to change:
- Colors and typography
- Layout and spacing
- Dark mode colors
- Responsive breakpoints

## Deployment on Tilde.club

1. Upload the files to your tilde.club home directory
2. Make sure `index.html` is in the public_html folder
3. The site will be available at `https://tilde.club/~yourresco`

## Local Development

To preview the site locally:
1. Open `index.html` in a web browser
2. Or use a local server: `python -m http.server 8000`

## License

This project is open source and available under the MIT License.

## Credits

Built with ❤️ for the tilde.club community. 