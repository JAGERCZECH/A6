self.addEventListener('push', function(event) {
    const data = event.data.json();
    const title = data.title;
    const options = {
        body: data.body,
        icon: '/path/to/icon.png',  // Optional: Add an icon for the notification
        badge: '/path/to/badge.png' // Optional: Add a badge for the notification
    };
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});
