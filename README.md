# 🗺️ TripCraft AI - AI-Powered Travel Planner

A comprehensive AI-powered travel planning application that helps users discover destinations, create detailed itineraries, and get personalized travel recommendations.

## ✨ Features

### 🎯 Core Features
- **AI Destination Recommendations** - Get personalized destination suggestions based on budget, travel style, and duration
- **Detailed Itinerary Generation** - AI creates day-by-day travel plans with activities, meals, and costs
- **TripAdvisor-Style Reviews** - Authentic traveler reviews and ratings for destinations
- **Direct Booking Links** - One-click access to hotels, flights, and activities
- **Restaurant Website Links** - Direct links to restaurant websites, menus, and booking
- **AI Travel Assistant Chatbot** - Conversational AI for travel questions and advice

### 🛠️ Technical Features
- **FastAPI Backend** - High-performance Python web framework
- **OpenAI Integration** - GPT-3.5-turbo for AI-powered recommendations
- **HTMX Frontend** - Dynamic, responsive interface without page reloads
- **Modern UI/UX** - Clean, intuitive design with smooth animations
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tripcraft-ai.git
   cd tripcraft-ai
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open your browser**
   Navigate to `http://localhost:8000`

## 📖 Usage

### 1. Get Destination Recommendations
- Fill out the form with your budget, travel style, and duration
- Get AI-generated destination suggestions with booking links

### 2. Generate Detailed Itineraries
- Click "Generate Itinerary" on any destination
- Receive day-by-day travel plans with activities and restaurant recommendations

### 3. Chat with AI Assistant
- Click the floating chatbot button (🤖)
- Ask any travel-related questions for personalized advice

### 4. Book Your Trip
- Use direct booking links for hotels, flights, and activities
- Access restaurant websites and make reservations

## 🏗️ Project Structure

```
tripcraft-ai/
├── app/
│   ├── main.py              # FastAPI application
│   ├── templates/           # HTML templates
│   │   ├── index.html       # Main page
│   │   ├── results.html     # Destination results
│   │   └── itinerary.html   # Itinerary display
│   └── static/              # Static files (CSS, JS, images)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Optional
```

### API Keys
- **OpenAI API Key**: Required for AI recommendations and chatbot
- **Anthropic API Key**: Optional, for additional AI capabilities

## 🌟 Features in Detail

### AI Destination Recommendations
- Personalized suggestions based on budget, style, and duration
- Real-time AI processing with fallback options
- Cost estimates and travel style matching

### Smart Itinerary Generation
- Day-by-day planning with specific activities
- Restaurant recommendations with direct links
- Cost breakdowns and time optimization

### TripAdvisor Reviews
- AI-generated authentic traveler reviews
- Star ratings and helpful tips
- Destination-specific insights

### Booking Integration
- Direct links to Booking.com, Expedia, and Viator
- Restaurant website and menu access
- One-click booking for activities

### AI Chatbot
- Conversational travel assistant
- Quick question buttons for common topics
- Real-time responses with typing indicators

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints
- `GET /` - Main application page
- `POST /recommend` - Get destination recommendations
- `POST /generate-itinerary` - Generate detailed itineraries
- `POST /chat` - AI chatbot endpoint

## 🚀 Deployment

### Deploy to Replit
1. Fork this repository to your GitHub account
2. Go to [replit.com](https://replit.com)
3. Click "Create Repl" and select "Import from GitHub"
4. Choose your forked repository
5. Add your environment variables in the Secrets tab
6. Click "Run" to deploy

### Deploy to Heroku
1. Create a `Procfile` with: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
2. Add your environment variables in Heroku dashboard
3. Deploy using Heroku CLI or GitHub integration

### Deploy to Railway
1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically on push

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the AI capabilities
- FastAPI for the excellent web framework
- HTMX for dynamic frontend interactions
- The travel community for inspiration and feedback

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Check the documentation
- Contact the development team

---

**Happy Traveling! ✈️🗺️**
