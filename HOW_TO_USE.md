# 📘 Cerberus DeepCrystal: How to Use Guide

Follow these steps to successfully launch and operate the Cerberus DeepCrystal AI Forensic Laboratory.

## 1. System Requirements
* **Python**: Version 3.10 or higher installed and added to your system PATH.
* **Node.js**: Version 18+ installed.
* **Internet Connection**: Required on the first run to download the HuggingFace AI models (~600MB payload).

## 2. Launching the System

You must start both the Backend (Python) and Frontend (React) servers. The project includes convenient batch scripts for Windows.

### Start the Backend
1. Open the project root folder.
2. Double-click **`start_backend.bat`**.
3. *What it does*: This script will install missing Python packages, seed the SQLite database with 29 known minerals, and launch the FastAPI server on `http://localhost:8000`. Leave the terminal window open.

### Start the Frontend
1. Go back to the project root folder.
2. Double-click **`start_frontend.bat`**.
3. *What it does*: This installs `npm` dependencies and launches the Vite development server. Leave the terminal window open.
4. Your default web browser should open automatically to `http://localhost:5173`. If not, click the link or type it into your browser.

## 3. Navigating the UI

When the app opens, you'll see a dark-purple clinical UI with a left-hand sidebar:
* **Dashboard**: View high-level metrics of your session, including average AI confidence and total scans.
* **Gem Scanner**: The primary interface. This is where you upload images and run the analysis.
* **Mineral Database**: A complete, searchable table of all supported gemstones containing chemical and optical properties.
* **Analysis History**: A record of every scan you have performed, including access to their unique Blockchain Certificate IDs.

## 4. How to Analyze a Gemstone

1. **Go to the Gem Scanner** tab.
2. **Upload an Image**: Drag and drop a clear, well-lit photo of the gemstone into the main upload box. (A plain white background yields the best AI results).
3. **Select Mode**: Choose "Lab Research Mode" (highest data output) or "Pro Dealer Mode."
4. **Enter Manual Data (Optional but Recommended)**: The AI is incredibly powerful, but true gemology requires physical data. Expand the "Manual Data" section to input the exact weight (Carats), Refractive Index (RI), Specific Gravity (SG), and Mohs Hardness if you know them. This dramatically increases the final confidence score and price accuracy.
5. **Click "Scan Gemstone"**.

> **⚠️ IMPORTANT FIRST RUN NOTE**: The very first time you click "Scan", the Python backend must load PyTorch and the CLIP neural network weights into RAM. This can take **15 to 45 seconds** depending on your CPU. Subsequent scans will be nearly instantaneous. 

## 5. Reviewing the Report
After scanning, the Report Dashboard generates automatically:
* **The Certificate Banner**: Shows your unique, immutable ID and a SHA-256 hash.
* **Identity Banner**: Displays the predicted gem name, chemical formula, and basic physical specs.
* **Confidence Meter**: Indicates how certain the Neural Network is of its classification.
* **Market Value**: Displays estimated USD and local (LKR) values based on carat weight, treatments, and natural probability.
* **Inclusions & Damage**: Shows heuristic assessments of cracks, gas bubbles, rutile silk, and other key identifying inner features.

---
*For troubleshooting, check the terminal windows where the `start_bat` files are running for detailed error logs.*
