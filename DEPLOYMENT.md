# 🚀 Deployment Guide

This guide will help you deploy TripCraft AI to GitHub and Replit.

## 📋 Prerequisites

- GitHub account
- Replit account
- OpenAI API key

## 1. GitHub Deployment

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository: `tripcraft-ai`
4. Make it **Public** (for Replit deployment)
5. **Don't** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Run these in your terminal:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tripcraft-ai.git

# Push your code to GitHub
git push -u origin main
```

### Step 3: Verify Deployment

1. Go to your repository URL: `https://github.com/YOUR_USERNAME/tripcraft-ai`
2. You should see all your files uploaded
3. The README.md will display on the repository page

## 2. Replit Deployment

### Step 1: Create Replit Project

1. Go to [Replit.com](https://replit.com) and sign in
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Choose your `tripcraft-ai` repository
5. Select "Python" as the language
6. Click "Import from GitHub"

### Step 2: Configure Environment Variables

1. In your Replit project, click on "Tools" in the left sidebar
2. Select "Secrets"
3. Add these environment variables:

```
OPENAI_API_KEY = your_openai_api_key_here
ANTHROPIC_API_KEY = your_anthropic_api_key_here
```

### Step 3: Install Dependencies

1. In the Replit shell, run:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

1. Click the "Run" button at the top
2. Replit will automatically run the application
3. You'll see a webview with your app running
4. The URL will be something like: `https://tripcraft-ai.yourusername.repl.co`

### Step 5: Share Your App

1. Click "Share" in the top right
2. Copy the URL to share with others
3. Your app is now live and accessible worldwide!

## 🔧 Troubleshooting

### Common Issues

**1. Module not found errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**2. API key errors**
- Verify your OpenAI API key is correct in the Secrets tab
- Make sure the key has sufficient credits

**3. Port issues**
- Replit automatically handles port configuration
- The app should run on the default port

**4. Import errors**
- Check that all files are in the correct directory structure
- Ensure `app/main.py` exists and is properly formatted

### Getting Help

- Check the Replit console for error messages
- Verify your environment variables are set correctly
- Make sure your GitHub repository is public (for Replit import)

## 🌐 Alternative Deployment Options

### Railway
1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard
3. Deploy automatically

### Heroku
1. Create a Heroku account
2. Install Heroku CLI
3. Run: `heroku create your-app-name`
4. Add environment variables: `heroku config:set OPENAI_API_KEY=your_key`
5. Deploy: `git push heroku main`

### Vercel
1. Connect your GitHub repository to Vercel
2. Configure as a Python project
3. Add environment variables
4. Deploy automatically

## 📱 Testing Your Deployment

After deployment, test these features:

1. **Homepage** - Should load the travel planner form
2. **Destination Recommendations** - Fill out the form and get AI suggestions
3. **Itinerary Generation** - Click "Generate Itinerary" on any destination
4. **Chatbot** - Click the floating 🤖 button and ask travel questions
5. **Booking Links** - Test the hotel, flight, and activity booking links

## 🔒 Security Notes

- Never commit your `.env` file to GitHub
- Use environment variables for all API keys
- Keep your API keys secure and don't share them publicly
- Monitor your API usage to avoid unexpected charges

## 📈 Monitoring

- Check your Replit usage and limits
- Monitor OpenAI API usage and costs
- Set up alerts for high usage if needed

---

**Your TripCraft AI is now deployed and ready to help travelers worldwide! 🌍✈️**
