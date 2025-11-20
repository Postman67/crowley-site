function viewQueue() {
    const serverIdInput = document.getElementById('server-id');
    const serverId = serverIdInput.value.trim();
    
    if (!serverId) {
        alert('Please enter a server ID');
        return;
    }
    
    // Validate that serverId contains only numbers
    if (!/^\d+$/.test(serverId)) {
        alert('Server ID must contain only numbers');
        return;
    }
    
    // Redirect to the queue page
    window.location.href = `/serverqueue/${serverId}`;
}

// Allow Enter key to trigger the search
document.addEventListener('DOMContentLoaded', function() {
    const serverIdInput = document.getElementById('server-id');
    serverIdInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            viewQueue();
        }
    });
});
