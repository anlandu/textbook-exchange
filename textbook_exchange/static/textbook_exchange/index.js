  // Get handle to the chat div
  var $chatWindow = $('#messages');
  console.log('Going to start a channel ' + channelName)
   
   // Our interface to the Chat service
   var chatClient;
 
   // A handle to the "general" chat channel - the one and only channel we
   // will have in this sample app
   var generalChannel;
 
   // The server will assign the client a random username - store that value
   // here
   var username;
 
   // Helper function to print info messages to the chat window
   function print(infoMessage, asHtml) {
     var $msg = $('<div class="info">');
     if (asHtml) {
       $msg.html(infoMessage);
     } else {
       $msg.text(infoMessage);
     }
     //$chatWindow.append($msg);
   }
 
  // Helper function to print chat message to the chat window
  function printMessage(fromUser, message) {
    let $container = "";
    if (fromUser === username) {
      $container = $('<div class="d-flex flex-row-reverse p-1">');
    } else {
      $container = $('<div class="d-flex flex-row p-1">');
    }
    
    var $message = $('<div class="p-2 bd-highlight" style="background: lightgray; border-radius: 15px;">').text(message);
    $container.append($message);
    $chatWindow.append($container);
    $chatWindow.scrollTop($chatWindow[0].scrollHeight);
  }
 
   // Alert the user they have been assigned a random username
   print('Logging in...');
 
   // Get an access token for the current user, passing a username (identity)
   // and a device ID - for browser-based apps, we'll always just use the
   // value "browser"
   $.getJSON('/token', {
     device: 'browser'
   }, function(data) {
     // Initialize the Chat client
      Twilio.Chat.Client.create(data.token).then(client => {
        console.log('Created chat client');
        chatClient = client;
        chatClient.on('channelInvited', function(channel) {
          console.log('Invited to channel ' + channel.friendlyName);
          try {
            channel.join();
          } catch (e) {
            console.log(e);
          }
        });
        chatClient.getChannelByUniqueName(channelName).then(function(channel) {
            generalChannel = channel;
            console.log('Found a channel: ');
            console.log(generalChannel);
            setupChannel();
        })      
     }).catch(error => {
       console.error(error);
       print('There was an error creating the chat client:<br/>' + error, true);
       print('Please check your .env file.', false);
     });
   });
 
   // Set up channel after it has been found
   function setupChannel() {
     // Join the general channel
     getChatHistory(generalChannel);
     // Listen for new messages sent to the channel
     generalChannel.on('messageAdded', function(message) {
       printMessage(message.author, message.body);
     });
   }
 
   function getChatHistory(channel) {
     // Get Messages for a previously created channel
     channel.getMessages().then(function(messages) {
     const totalMessages = messages.items.length;
     for (i = 0; i < totalMessages; i++) {
       const message = messages.items[i];
       printMessage(message.author, message.body);
     }
     console.log('Total Messages:' + totalMessages);
     });
   }

   // Send a new message to the general channel
   var $input = $('#chat-input');
   $input.on('keydown', function(e) {
 
     if (e.keyCode == 13) {
       if (generalChannel === undefined) {
         print('The Chat Service is not configured. Please check your .env file.', false);
         return;
       }
       generalChannel.sendMessage($input.val())
       $input.val('');
     }
   });

