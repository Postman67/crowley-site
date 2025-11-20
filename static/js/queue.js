// Get server ID from the page
const serverId = document.getElementById('server-id').textContent;

// Format duration from milliseconds to MM:SS
function formatDuration(milliseconds) {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

// Format requester ID (you could enhance this to fetch username if needed)
function formatRequester(song) {
    // If we have the Discord username, use it
    if (song.requester_name) {
        return `🎤 ${song.requester_name}`;
    }
    // Otherwise show the user ID
    return `👤 User: ${song.requester}`;
}

// Fetch and display the queue
async function loadQueue() {
    const queueContainer = document.getElementById('queue-container');
    
    try {
        const response = await fetch(`/api/queue/${serverId}`);
        const data = await response.json();
        
        if (!data.success) {
            queueContainer.innerHTML = `
                <div class="error">
                    Error loading queue: ${data.error}
                </div>
            `;
            return;
        }
        
        const queue = data.queue;
        
        // Update page title and server name if available
        if (data.server_name) {
            document.querySelector('h1').textContent = `Music Queue`;
            const serverNameElement = document.getElementById('server-name');
            serverNameElement.textContent = data.server_name;
            serverNameElement.style.display = 'block';
        }
        
        if (queue.length === 0) {
            queueContainer.innerHTML = `
                <div class="empty-queue">
                    <p>🎵 The queue is currently empty</p>
                </div>
            `;
            return;
        }
        
        // Build the queue list
        let queueHTML = '<ul class="queue-list">';
        
        queue.forEach((song, index) => {
            queueHTML += `
                <li class="queue-item">
                    <span class="queue-item-number">${index + 1}</span>
                    <div class="song-info">
                        <div class="song-title">${escapeHtml(song.title)}</div>
                        <div class="song-author">by ${escapeHtml(song.author)}</div>
                        <div class="song-details">
                            <span class="song-duration">⏱️ ${formatDuration(song.duration)}</span>
                            <span class="song-requester">${formatRequester(song)}</span>
                            ${song.uri ? `<a href="${escapeHtml(song.uri)}" target="_blank" class="song-link">🎵 Open in Spotify</a>` : ''}
                        </div>
                    </div>
                </li>
            `;
        });
        
        queueHTML += '</ul>';
        queueContainer.innerHTML = queueHTML;
        
    } catch (error) {
        queueContainer.innerHTML = `
            <div class="error">
                Error loading queue: ${error.message}
            </div>
        `;
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-refresh the queue every 5 seconds
function startAutoRefresh() {
    setInterval(loadQueue, 5000);
}

// Load queue on page load
document.addEventListener('DOMContentLoaded', function() {
    loadQueue();
    startAutoRefresh();
});
