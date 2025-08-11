# Indian Language to Braille Translator (FastAPI + React)

A full-stack application that converts Indian language text into Braille.  
Supports multiple Indian languages using **liblouis** translation tables, with options for plain text output and downloadable Braille PDFs.

---

## 🚀 Features

- Convert Indian language text to Braille using **liblouis**.
- Supports multiple Indian languages:
  - Hindi (`hi-in-g1.utb`)
  - Tamil (`ta-in-g1.utb`)
  - Malayalam (`ml-in-g1.utb`)
  - Marathi (`mr-in-g1.utb`)
  - Bengali (`bn-in-g1.utb`)
- Download Braille output as PDF.
- Modern frontend built with React + Vite.
- Backend API built with FastAPI, including CORS support for frontend development.

---

## 📂 Key Files

---

braille_app/\
├── backend/   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                  # FastAPI backend\
│   ├── main.py &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;               # API endpoints\
│   ├── requirements.txt &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       # Backend dependencies\
│   └── braille_utils.py  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     # Braille conversion logic\
│\
├── src/  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                     # React frontend\
│   ├── App.jsx        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       # Main React component\
│   ├── components/\
│   │   ├── useBraille.js   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  # Hook for fetching Braille text\
│   │   ├── useBraillePDF.js &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Hook for downloading Braille as PDF\
│   │   └── useBrailleFile.js &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # Hook for file-based Braille conversion\
│   └── main.jsx    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         # Entry point\
│\
└── README.md

---

## 📝 Overview

This project offers:

- A REST API (FastAPI) to convert Indian language text to Braille.
- API endpoints for both text and PDF Braille output.
- Frontend React interface to interact with the API.
- Support for Braille conversion of uploaded text files.

---

## ⚙️ Backend Setup

1. Navigate to the backend directory:

    ```bash
    cd backend
    ```

2. Create and activate a Python virtual environment:

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

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the FastAPI server (development mode):

    ```bash
    uvicorn main:app --reload --port 8001
    ```

5. The API will be available at:  
   [http://127.0.0.1:8001](http://127.0.0.1:8001)

---

## ⚙️ Frontend Setup (React + Vite)

1. Navigate to the frontend directory:

    ```bash
    cd braille_app
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the development server:

    ```bash
    npm run dev
    ```

4. Open your browser at the URL shown in the terminal (typically `http://localhost:3000`).

---

## 🔗 Usage

- Enter text in any supported Indian language.
- Choose the desired Braille translation table.
- View the Braille output on the screen.
- Download the Braille output as a PDF.
- Optionally, upload text files for Braille conversion.

---

## 📚 Dependencies

- Backend:
  - FastAPI
  - Uvicorn
  - liblouis (Python bindings)
  - python-multipart
  - aiofiles
- Frontend:
  - React
  - Vite

---

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
GPL-3.0 License Summary
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.

What this means
You are free to:

✅ Use this software for any purpose
✅ Study how the program works and modify it
✅ Distribute copies to help others
✅ Distribute copies of your modified versions to others

Under these conditions:

📋 Copyleft - If you distribute this software or derivatives, you must make the source code available under GPL-3.0
📄 License and copyright notice - Include the original license and copyright notice
🔄 State changes - Document any changes you make to the original code
🚫 No additional restrictions - You cannot impose additional restrictions on recipients

This ensures:

The software and its derivatives remain free and open source
Improvements benefit the entire community
Accessibility tools like this Braille converter stay available to everyone

Contributing
By contributing to this project, you agree that your contributions will be licensed under the GPL-3.0 License.

---

## Author

Parv Gheewala - codespacetechlabs

---
