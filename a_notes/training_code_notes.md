# Weather Chat App 
## files src/app.py and src/sec5_sqlite.py
## data flow
1. user calls agent
2. agent calls get_weather
3. get_weather calls get_location
4. get_location calls javascript to find out user location
5. the flow goes backwards with the info

## Javascript to get location - en templates/chat.html
* User must give access to the browser to share location
* session obj instance is passed through python modules automagically
<script>
        // Get user's location once when page loads
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                document.getElementById('latitude').value = position.coords.latitude;
                document.getElementById('longitude').value = position.coords.longitude;
            });
        }
    </script>
