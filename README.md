# 🌟 AI Vedic Astrologer

An intelligent Vedic astrology application that provides personalized readings using AI-powered analysis. This Streamlit-based web app combines traditional Vedic astrology calculations with modern AI to deliver comprehensive astrological insights.

## ✨ Features

- **🔮 Personalized Vedic Readings**: Generate detailed astrological readings based on birth details
- **🤖 AI-Powered Analysis**: Uses Google Gemini AI for intelligent interpretation of astrological data
- **📊 Interactive Chart Generation**: Create and download beautiful Vedic astrology charts
- **💬 Chat Interface**: Ask follow-up questions and get detailed answers
- **🌍 Global Location Support**: Automatic timezone and coordinate detection
- **📱 User-Friendly Interface**: Clean, intuitive Streamlit web interface


## 🛠️ Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection for ephemeris data and API calls

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai_astrologer.git
cd ai_astrologer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Google Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note**: You can get a free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## 🔧 Setup Instructions

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Paste it in your `.env` file

### 2. Install Swiss Ephemeris

The application automatically downloads and sets up Swiss Ephemeris data for accurate astronomical calculations. This happens automatically when you first run the app.

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## 📱 Usage Guide

### 1. Enter Birth Details

- **Date of Birth**: Format: DD/MM/YYYY (e.g., 09/01/2000)
- **Time of Birth**: Format: HH:MM:SS (e.g., 14:30:00)
- **Place of Birth**: City, State/Country (e.g., New York, NY)
- **Your Name**: For personalized readings

### 2. Generate Reading

Click "Generate Reading" to calculate your Vedic horoscope. The app will:
- Calculate planetary positions
- Determine house placements
- Compute Vimshottari Dasa periods
- Analyze planetary and house significators

### 3. Get AI Reading

Click "🔮 Get Detailed Reading" to receive a comprehensive AI-generated interpretation of your chart.

### 4. Ask Questions

Use the chat interface to ask specific questions about:
- Career prospects
- Relationship compatibility
- Health matters
- Financial outlook
- And more!

### 5. Generate Chart

Click "🎨 Generate Chart Image" to create a visual representation of your Vedic chart that you can download.

## 🏗️ Architecture

The application is built with:

- **Frontend**: Streamlit for the web interface
- **AI Engine**: Google Gemini 2.0 Flash for intelligent readings
- **Astrology Engine**: VedicAstro library for calculations
- **Ephemeris**: Swiss Ephemeris for planetary positions
- **Geocoding**: Nominatim for location services
- **Timezone**: TimezoneFinder for accurate time calculations

## 📁 Project Structure

```
ai_astrologer/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md            # This file
└── .gitignore           # Git ignore file
```

## 🔑 Key Components

- **VedicHoroscopeData**: Core astrology calculation engine
- **Swiss Ephemeris**: Astronomical data for planetary positions
- **AI Integration**: Gemini-powered interpretation system
- **Chart Generation**: Visual chart creation and export
- **Location Services**: Automatic coordinate and timezone detection

## 🌟 Features in Detail

### AI-Powered Readings
- Personalized interpretations based on your unique birth chart
- Context-aware responses to follow-up questions
- Comprehensive analysis of planetary positions and house placements

### Chart Generation
- Professional-quality Vedic astrology charts
- Downloadable PNG format
- Accurate planetary and house cusp positions

### Global Support
- Automatic timezone detection
- Worldwide location support
- Accurate calculations for any birth location



## 🔮 Future Enhancements

- [ ] Multiple chart types (North Indian, South Indian, Western)
- [ ] Transit predictions
- [ ] Compatibility analysis
- [ ] Muhurta (auspicious timing) calculations
- [ ] Mobile app version
- [ ] Multi-language support


**Disclaimer**: This application is for entertainment and educational purposes only. Astrological readings should not replace professional advice in matters of health, finance, or legal decisions.

---

⭐ **Star this repository if you find it helpful!** 
