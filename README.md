# Contributing to Bharti2Braille

Thank you for your interest in contributing to the Indian Language to Braille Translator! 🙏  
We welcome contributions from everyone—whether it's fixing bugs, adding features, improving documentation, or suggesting enhancements.  

By contributing, you agree to follow our guidelines for a smooth collaboration and that your contributions will be licensed under the GPL-3.0 License.

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Branching & Workflow](#branching--workflow)
8. [Issue Reporting](#issue-reporting)
9. [Adding New Language Support](#adding-new-language-support)
10. [Code of Conduct](#code-of-conduct)
11. [License](#license)

---

## Getting Started

1. **Fork the repository** to your GitHub account.  
2. **Clone your fork** locally:

```bash
git clone https://github.com/<your-username>/Bharti2Braille.git
cd Bharti2Braille
```

---

## Project Structure

Understanding the project structure will help you navigate and contribute effectively:

```
braille_app/
├── backend/                          # FastAPI backend
│   ├── braille_api.py                # Braille text translation API (port 8000)
│   ├── braille_pdf_api.py            # Braille PDF generation API (port 8001)
│   ├── requirements.txt              # Backend dependencies
│   └── fonts/                        # Font files for PDF generation
│       ├── NotoSansDevanagari-Regular.ttf
│       └── NotoSansSymbols2-Regular.ttf
│
├── src/                              # React frontend
│   ├── App.jsx                       # Main React component
│   ├── components/
│   │   ├── useBraille.js             # Hook for fetching Braille text
│   │   ├── useBraillePDF.js          # Hook for downloading Braille as PDF
│   │   └── useBrailleFile.js         # Hook for file-based Braille conversion
│   └── main.jsx                      # Entry point
│
└── README.md
```

---

## Development Setup

### Backend Setup (FastAPI)

1. **Navigate to the backend directory**:
```bash
cd backend
```

2. **Create and activate a Python virtual environment**:
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - On Windows:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install required dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install liblouis** (Braille translation engine):
   - Download the Windows build from [liblouis downloads](https://liblouis.io/downloads/) — use `liblouis-3.37.0-win64.zip` for 64-bit Windows
   - Extract and note the full path to `lou_translate.exe` inside the `bin\` folder
   - Set the `LOU_TRANSLATE` variable at the top of both `braille_api.py` and `braille_pdf_api.py`:
     ```python
     LOU_TRANSLATE = r"C:\path\to\liblouis-3.37.0-win64\bin\lou_translate.exe"
     ```

5. **Add font files** for PDF generation:
   - Create a `fonts/` folder inside `backend/`
   - Download and place the following fonts inside it:
     - `NotoSansDevanagari-Regular.ttf` from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari)
     - `NotoSansSymbols2-Regular.ttf` from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Symbols+2)

6. **Run the two backend servers** (open two separate terminals):

   *Terminal 1 — Braille text API (port 8000):*
   ```bash
   uvicorn braille_api:app --reload --port 8000
   ```

   *Terminal 2 — Braille PDF API (port 8001):*
   ```bash
   uvicorn braille_pdf_api:app --reload --port 8001
   ```

7. The APIs will be available at:
   - Text API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - PDF API: [http://127.0.0.1:8001](http://127.0.0.1:8001)

### Frontend Setup (React + Vite)

1. **Navigate to the project root**:
```bash
cd braille_app
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start the development server**:
```bash
npm run dev
```

4. Open your browser at the URL shown in the terminal (typically `http://localhost:5173`).

---

## How to Contribute

1. **Create a new branch** for your changes:
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** with clear and concise code.

3. **Run tests** to ensure nothing breaks.

4. **Commit your changes**:
```bash
git commit -m "Add meaningful description of your change"
```

5. **Push your branch**:
```bash
git push origin feature/your-feature-name
```

6. **Open a Pull Request (PR)** on the main repository:
   * Describe what you changed and why.
   * Link any related issues, if applicable.
   * Ensure both backend and frontend work correctly together.

---

## Coding Standards

### Python (Backend)
- Use **4 spaces** for indentation (no tabs).
- Follow **PEP8** for Python code.
- Use **clear variable and function names**.
- Keep functions **small and focused**.
- Write **docstrings** for new functions or classes.
- Use type hints where appropriate.

### JavaScript/React (Frontend)
- Use **2 spaces** for indentation.
- Use **ES6+ features** and modern React patterns.
- Follow **functional component patterns** with hooks.
- Use **clear component and variable names**.
- Keep components **small and reusable**.

### General
- Write **meaningful commit messages**.
- Keep **dependencies minimal** and up-to-date.
- **Comment complex logic** clearly.

---

## Testing

- Ensure all existing tests pass before submitting a PR.
- Add **new tests** for new features or bug fixes.
- Test both **backend API endpoints** and **frontend components**.
- Run backend tests using:
```bash
pytest
```
- Test frontend functionality manually and with any existing test suite.

---

## Branching & Workflow

- **main**: Stable, production-ready code.
- **develop**: Latest development code (if applicable).
- **feature/**: Feature branches (e.g., `feature/add-gujarati-support`).
- **bugfix/**: Bug fix branches (e.g., `bugfix/pdf-generation-error`).
- **docs/**: Documentation updates (e.g., `docs/update-contributing-guide`).

**Always create a branch from** `main` (or `develop` if using GitFlow).

---

## Issue Reporting

Before opening an issue, **search existing issues** to avoid duplicates.

### For Bugs
Provide the following in your issue:
- Clear **title** describing the problem.
- Steps to **reproduce** the bug.
- **Expected vs. actual behavior**.
- Screenshots or error logs, if relevant.
- **Environment details** (OS, browser, Python version, etc.).

### For Feature Requests
- Clear **description** of the proposed feature.
- **Use case** and why it would be valuable.
- Any **implementation ideas** or suggestions.

### For Language Support Requests
- **Language name** and ISO code.
- **Liblouis table name** (if known).
- **Sample text** for testing.

---

## Adding New Language Support

Our project currently supports:
- Hindi (`hi-in-g1.utb`)
- Tamil (`ta-in-g1.utb`)
- Malayalam (`ml-in-g1.utb`)
- Marathi (`mr-in-g1.utb`)
- Bengali (`bn-in-g1.utb`)
- Gujarati (`gu-in-g1.utb`)

### To Add a New Language:

1. **Check liblouis compatibility**: Ensure the language has a liblouis translation table.

2. **Update backend** (`backend/braille_api.py` and `backend/braille_pdf_api.py`):
   - Add the new language to the `SUPPORTED_TABLES` dictionary.
   - Add the corresponding liblouis table filename.

3. **Update frontend** (`src/App.jsx`):
   - Add the new language option to the `languageTables` object.
   - Ensure proper language name display.

4. **Test thoroughly**:
   - Test with sample text in the new language.
   - Verify PDF generation works correctly.
   - Test file upload functionality.

5. **Update documentation**:
   - Add the new language to the README.md supported languages list.
   - Update any relevant documentation.

### Language Table Resources:
- [Liblouis Tables Repository](https://github.com/liblouis/liblouis/tree/master/tables)
- [Language codes reference](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

---

## Code of Conduct

We expect everyone to:
- Be **respectful and constructive** in all interactions.
- **Welcome newcomers** and help them get started.
- **Give constructive feedback** on code and ideas.
- Avoid **offensive language** or discriminatory behavior.
- **Focus on accessibility** - remember this project serves people with visual impairments.

Violations may result in removal from the project.

---

## Development Tips

### Working with Braille Conversion
- Test with **real Indian language text** to ensure accuracy.
- Verify **Unicode handling** is correct for different scripts.
- Check that **PDF generation** maintains proper Braille formatting.

### API Development
- Follow **RESTful principles** for new endpoints.
- Include proper **error handling** and status codes.
- Add **CORS support** for frontend development.
- Document new endpoints clearly.

### Frontend Development
- Ensure **accessibility** features are maintained.
- Test with **different screen readers** if possible.
- Keep the interface **simple and intuitive**.
- Consider **mobile responsiveness**.

---

## Getting Help

- **Check existing issues** and documentation first.
- **Open a discussion** for questions about implementation approaches.
- **Tag maintainers** in PRs that need review.
- Be **patient and respectful** when asking for help.

---

## License

This project is licensed under the **GNU General Public License v3.0**.

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License, which ensures:
- The software and its derivatives remain **free and open source**.
- **Improvements benefit the entire community**.
- **Accessibility tools** like this Braille converter stay available to everyone.

For more details, see the [LICENSE](LICENSE) file or visit [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html).

---

## Acknowledgments

Thank you for helping make **Bharti2Braille** better! 💜

Your contributions help make digital content more accessible to the visually impaired community across India and beyond.

---

**Author**: Parv Gheewala - codespacetechlabs  
**Project**: Indian Language to Braille Translator