# CV Builder 📝

An interactive web application that allows users to create professional resumes from JSON data with multiple templates and export options.

## ✨ Features

- 🎨 **Multiple Templates**: Choose from various professional CV templates (Classic, Modern, Minimal)
- 🔧 **Interactive Editor**: User-friendly web interface for editing CV data
- 👀 **Live Preview**: Real-time preview of your CV as you edit
- 📄 **PDF Export**: Export your CV as a high-quality PDF
- 📦 **Project Download**: Download a complete project ready for GitHub Pages deployment
- 🎯 **JSON Schema**: Uses standardized JSON Resume schema for data portability
- 📱 **Responsive**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Option 1: Interactive Web Interface (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/AndresKenji/andreskenji.github.io.git
   cd andreskenji.github.io
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the web application**
   ```bash
   python main.py --web
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000` and start building your CV!

### Option 2: Command Line (Traditional)

1. **Edit your data**
   Modify `src/data/resume.json` with your information

2. **Generate CV**
   ```bash
   python main.py
   ```

3. **View result**
   Open `docs/index.html` in your browser

## 📁 Project Structure

```
├── app/                          # Web application
│   ├── cv-templates/            # CV templates
│   │   ├── classic/            # Classic template
│   │   ├── modern/             # Modern template
│   │   └── minimal/            # Minimal template
│   ├── static/                 # Static assets (CSS, JS, images)
│   └── templates/              # HTML templates
├── src/                         # Core functionality
│   ├── data/                   # Resume data
│   ├── models.py              # Data models
│   ├── render.py              # Template rendering
│   └── template_manager.py    # Template management
├── docs/                       # Generated CV output
├── main.py                     # Main application
├── app.py                      # Flask web app
└── requirements.txt           # Dependencies
```

## 🎨 Available Templates

### Classic Template
- Professional and clean design
- Sidebar with contact info and skills
- Traditional layout perfect for corporate environments

### Modern Template (Coming Soon)
- Contemporary design with modern elements
- Gradient accents and card-based layout
- Perfect for creative and tech roles

### Minimal Template (Coming Soon)
- Clean and minimalist design
- Focus on content over decoration
- Great for academic and research positions

## 🔧 Customization

### Adding New Templates

1. Create a new directory in `app/cv-templates/`
2. Add the required files:
   - `template.json` - Template metadata
   - `layout.html` - Main template file
   - `sidebar.html` - Sidebar component
   - `main.html` - Main content component
   - `static/css/styles.css` - Template styles

### Template Structure

```json
{
  "name": "Template Name",
  "description": "Template description",
  "author": "Your Name",
  "version": "1.0.0",
  "features": ["Feature 1", "Feature 2"],
  "colors": {
    "primary": "#color1",
    "secondary": "#color2",
    "accent": "#color3"
  }
}
```

## 📊 JSON Schema

This project follows the [JSON Resume](https://jsonresume.org/) schema with some extensions. The main sections include:

- **basics**: Personal information, contact details
- **work**: Work experience
- **education**: Educational background
- **skills**: Technical and soft skills
- **languages**: Language proficiencies
- **interests**: Hobbies and interests
- **volunteer**: Volunteer experience
- **awards**: Awards and recognitions
- **publications**: Publications and papers
- **projects**: Personal and professional projects

## 🚀 Deployment to GitHub Pages

When you download a project from the web interface, you get a complete setup ready for GitHub Pages:

1. **Upload to GitHub**: Create a new repository and push the downloaded files
2. **Enable Pages**: Go to Settings > Pages in your repository
3. **Configure**: Select "Deploy from a branch" and choose "main" branch with "/docs" folder
4. **Access**: Your CV will be available at `https://yourusername.github.io/repository-name`

## 🛠️ Development

### Setting up development environment

1. **Clone and install dependencies**
   ```bash
   git clone https://github.com/AndresKenji/andreskenji.github.io.git
   cd andreskenji.github.io
   pip install -r requirements.txt
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Run in development mode**
   ```bash
   python main.py --web
   ```

### Adding Features

- **Backend**: Modify `app.py` for new API endpoints
- **Frontend**: Update `app/static/js/app.js` for new functionality
- **Styles**: Edit `app/static/css/app.css` for styling changes
- **Templates**: Add new CV templates in `app/cv-templates/`

## 📋 Requirements

- Python 3.8+
- Flask
- Jinja2
- Pydantic
- WeasyPrint (for PDF generation)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [JSON Resume](https://jsonresume.org/) for the schema inspiration
- [Vue.js](https://vuejs.org/) for the reactive frontend
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [WeasyPrint](https://weasyprint.org/) for PDF generation

## 📞 Support

If you have any questions or need help, please:

1. Check the [Issues](https://github.com/AndresKenji/andreskenji.github.io/issues) page
2. Create a new issue if your question isn't already answered
3. Provide as much detail as possible when reporting bugs

---

**Made with ❤️ by [AndresKenji](https://github.com/AndresKenji)**