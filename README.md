# 🍳 AI Recipe Generator

An intelligent recipe generation app powered by OpenAI's GPT-4 and Streamlit. Transform your available ingredients into delicious, customized recipes with dietary preferences and cuisine options.

## ✨ Features

- **AI-Powered Recipe Generation**: Uses GPT-4 Turbo to create unique recipes
- **Ingredient-Based**: Generate recipes based on ingredients you have
- **Customization Options**:
  - Meal Type (Breakfast, Lunch, Dinner, Snack, Dessert)
  - Cuisine Selection (Nigerian, Italian, Chinese, Mexican, Indian, French, Japanese)
  - Servings Adjustment
  - Dietary Preferences (Vegetarian, Vegan, Gluten-Free)
- **Save Favorites**: Bookmark your favorite recipes for quick access
- **Recipe History**: Keep track of recently generated recipes
- **Download & Share**: Download recipes as text or share directly on WhatsApp
- **Beautiful UI**: Modern, responsive design with intuitive navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yakubnusaiba/recipe-generator.git
   cd recipe-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   Open your browser to `http://localhost:8501`

## 🌐 Deployment Options

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your `OPENAI_API_KEY` in Secrets
5. Deploy! 🚀

### Docker

Build and run the app in a container:

```bash
docker build -t recipe-generator .
docker run -p 8501:8501 recipe-generator
```

### Heroku

Use the included `Procfile` for Heroku deployment:

```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

## 📋 Usage

1. **Enter Ingredients**: List the ingredients you have (comma-separated)
2. **Select Preferences**: Choose meal type, cuisine, and dietary options
3. **Generate Recipe**: Click "✨ Generate Recipe"
4. **View & Interact**:
   - Read the full recipe
   - Save to favorites (❤️)
   - Download as text file
   - Share on WhatsApp
5. **Explore History**: View recently generated recipes in the sidebar

## 🏗️ Project Structure

```
recipe-generator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── .dockerignore            # Docker ignore file
├── Procfile                 # Heroku deployment config
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## 🛠️ Technologies

- **Streamlit**: Web app framework
- **OpenAI GPT-4 Turbo**: AI recipe generation
- **Python 3.8+**: Backend language

## 💡 Tips

- Be specific with ingredients for better recipes
- Mix and match dietary preferences
- Save your favorite recipes for future reference
- Share interesting recipes with friends

## 🐛 Troubleshooting

### API Key Not Set
```
OpenAI API key not set. Please add it to Streamlit secrets.
```
**Solution**: Add `OPENAI_API_KEY` to `.streamlit/secrets.toml` or Streamlit Cloud secrets

### Recipe Generation Failed
- Check your OpenAI API quota
- Verify API key is valid
- Try with fewer ingredients or simpler preferences

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📧 Support

For issues or questions, please open a GitHub issue or contact the maintainer.

---

**Made with ❤️ by yakubnusaiba**

*Happy Cooking! 🍳*
