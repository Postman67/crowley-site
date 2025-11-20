# Discord Music Bot Queue Viewer

A simple web application to visualize Discord music bot queues stored in Redis.

## Features

- View music queue for any Discord server
- **Automatic Discord name resolution** - Shows actual server names and usernames
- Real-time updates (auto-refreshes every 5 seconds)
- Clean, responsive design
- Displays song title, author, duration, and requester
- Direct links to Spotify tracks
- **Smart caching** - Discord names are cached to avoid rate limits

## Project Structure

```
crowley-site/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html        # Home page
│   └── queue.html        # Queue display page
└── static/
    ├── css/
    │   └── style.css     # Styles
    └── js/
        ├── index.js      # Home page logic
        └── queue.js      # Queue display logic
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. **Set up Discord Bot Token (Optional but recommended):**
   - Go to https://discord.com/developers/applications
   - Create a new application or select your existing bot
   - Go to the "Bot" section and copy your bot token
   - Set it as an environment variable:
   ```bash
   export DISCORD_BOT_TOKEN="your_bot_token_here"
   ```
   - **Note:** Your bot must be a member of the servers you want to query names for
   - Without this token, the app will show IDs instead of names

3. Make sure your Redis server is accessible at `192.168.1.225:6379`

4. Run the application:
```bash
python app.py
```

5. Access the site at `http://localhost:5050`

## Usage

1. Go to the home page
2. Enter a Discord server ID
3. Click "View Queue" to see that server's music queue

Or directly access: `http://localhost:5050/serverqueue/YOUR_SERVER_ID`

## Discord API Integration

The application automatically fetches real server names and usernames from Discord using the Discord API. Here's how it works:

1. **Server Names**: When you view a queue, the app fetches the actual server name
2. **User Names**: Each requester is shown with their Discord username
3. **Caching**: Names are cached in memory to avoid hitting Discord's rate limits
4. **Fallback**: If the Discord API is unavailable or no token is set, IDs are shown instead

### Getting a Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" or select an existing one
3. Go to the "Bot" section in the left sidebar
4. Click "Reset Token" or "Copy" to get your bot token
5. **Important**: Your bot must be invited to the servers you want to query
6. Add the token to your environment before running the app

## Redis Data Format

The application expects queue data in Redis with:
- Key format: `queue:{server_id}`
- Data type: List
- Each item is a JSON string with:
  - `title`: Song title
  - `author`: Artist name
  - `uri`: Spotify URL
  - `duration`: Duration in milliseconds
  - `requester`: Discord user ID

Example entry:
```json
{
  "title": "Hoist the Colours",
  "uri": "https://open.spotify.com/track/3p9jWNolR2X62CCKIb7Cih",
  "author": "Colm R. McGuinness",
  "duration": 122699,
  "requester": 615404299165499434
}
```
