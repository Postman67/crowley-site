from flask import Flask, render_template, jsonify
import redis
import json
import os
import requests
from functools import lru_cache

# Import manual server/user mappings
try:
    from server_mappings import SERVERS, USERS
except ImportError:
    SERVERS = {}
    USERS = {}

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host='192.168.1.225', port=6379, decode_responses=True)

# Discord Bot Token - set this as an environment variable
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN', '')
DISCORD_API_BASE = 'https://discord.com/api/v10'

# Cache for Discord API calls (cache for 1 hour)
@lru_cache(maxsize=1000)
def get_guild_name(guild_id):
    """Fetch guild (server) name from Discord API or manual mapping"""
    # First check manual mappings
    if str(guild_id) in SERVERS:
        return SERVERS[str(guild_id)]
    
    # Fall back to Discord API if bot token is available
    if not DISCORD_BOT_TOKEN:
        return None
    
    try:
        headers = {
            'Authorization': f'Bot {DISCORD_BOT_TOKEN}'
        }
        response = requests.get(
            f'{DISCORD_API_BASE}/guilds/{guild_id}',
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('name')
    except Exception as e:
        print(f"Error fetching guild name: {e}")
    return None

@lru_cache(maxsize=5000)
def get_user_name(user_id):
    """Fetch user name from Discord API or manual mapping"""
    # First check manual mappings
    if str(user_id) in USERS:
        return USERS[str(user_id)]
    
    # Fall back to Discord API if bot token is available
    if not DISCORD_BOT_TOKEN:
        return None
    
    try:
        headers = {
            'Authorization': f'Bot {DISCORD_BOT_TOKEN}'
        }
        response = requests.get(
            f'{DISCORD_API_BASE}/users/{user_id}',
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            username = data.get('username')
            # Discord removed discriminators for most users, but handle both cases
            discriminator = data.get('discriminator')
            if discriminator and discriminator != '0':
                return f"{username}#{discriminator}"
            return username
    except Exception as e:
        print(f"Error fetching user name: {e}")
    return None

def get_bot_status(bot_id):
    """Fetch bot status from Discord API or manual mapping"""
    # First check if we have a manual name for this bot
    bot_name = USERS.get(str(bot_id), "Crowley Music Bot")
    
    # Try to get status from Discord API if token is available
    if DISCORD_BOT_TOKEN:
        try:
            headers = {
                'Authorization': f'Bot {DISCORD_BOT_TOKEN}'
            }
            response = requests.get(
                f'{DISCORD_API_BASE}/users/{bot_id}',
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                username = data.get('username', bot_name)
                # Check if bot flag is present
                is_bot = data.get('bot', False)
                return {
                    'name': username,
                    'status': 'online',
                    'is_bot': is_bot
                }
        except Exception as e:
            print(f"Error fetching bot status: {e}")
    
    # Return default values if API is unavailable
    return {
        'name': bot_name,
        'status': 'unknown',
        'is_bot': True
    }

@app.route('/')
def index():
    bot_id = '1365530615272706128'
    bot_info = get_bot_status(bot_id)
    return render_template('index.html', bot_info=bot_info)

@app.route('/serverqueue/<server_id>')
def server_queue(server_id):
    # Try to get the server name for better meta tags
    guild_name = get_guild_name(server_id)
    page_title = f"Music Queue - {guild_name}" if guild_name else f"Music Queue - Server {server_id}"
    description = f"View the current music queue for {guild_name}" if guild_name else f"View the current music queue for server {server_id}"
    
    return render_template('queue.html', 
                         server_id=server_id,
                         page_title=page_title,
                         page_description=description)

@app.route('/api/queue/<server_id>')
def get_queue(server_id):
    try:
        # Fetch queue data from Redis
        # Assuming the key format is something like "music_queue:{server_id}"
        queue_key = f"music_queue:{server_id}"
        queue_data = redis_client.lrange(queue_key, 0, -1)
        
        # Parse JSON strings to objects
        queue = []
        for item in queue_data:
            try:
                song_data = json.loads(item)
                
                # Enrich with Discord usernames if available
                if 'requester' in song_data:
                    user_name = get_user_name(str(song_data['requester']))
                    if user_name:
                        song_data['requester_name'] = user_name
                
                queue.append(song_data)
            except json.JSONDecodeError:
                continue
        
        # Get guild name if available
        guild_name = get_guild_name(server_id)
        
        return jsonify({
            'success': True,
            'server_id': server_id,
            'server_name': guild_name,
            'queue': queue
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
