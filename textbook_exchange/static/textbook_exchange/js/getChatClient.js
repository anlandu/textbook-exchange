console.log("login successful; creating client")
$.getJSON('/token', {
    device: 'browser'
    }, function(data) {

    // Initialize the Chat client
    Twilio.Chat.Client.create(data.token).then(client => {
        console.log('Created chat client');
        chatClient = client;
        chatClient.on('channelInvited', function(channel) {
        console.log('Invited to channel ' + channel.friendlyName);
        if(channel.state.status !== "joined") 
            channel.join().then(function(channel) {
            console.log("joined channel" + channel.friendlyName);
                redirect(channel.uniqueName);
            });
        });
    }).catch(error => {
        console.error(error);
    });
    });