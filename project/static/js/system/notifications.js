setInterval(function () {
    $.ajax({
        url: '/core/api/user_messages/',
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            html = '';
            total_notifications = response.count;
            var notifications = response.results;
            for (var i = 0; i < notifications.length; i++) {
                var notification = notifications[i];
                var title = notification.title;
                var message = notification.message;
                var message_id = notification.id;
                var link = notification.link;
                var created_at = notification.created_at;
               
                html += '' +
                    '<a href="/core/messages/view/'+message_id+'"  class="text-reset notification-item"> ' +
                    '<div class="d-flex">' +
                    '    <div class="flex-shrink-0 avatar-sm me-3">' +
                    '        <span class="avatar-title bg-primary rounded-circle font-size-16">' +
                    '            <i class="bx bx-message-dots"></i>' +
                    '        </span>' +
                    '    </div>' +
                    '    <div class="flex-grow-1">' +
                    '        <h6 class="mb-1">' + title + '</h6>' +
                    '        <div class="font-size-13 text-muted">' +
                    '            <p class="mb-1">' + message + '</p>' +
                    '            <p class="mb-0"><i class="mdi mdi-clock-outline"></i> <span>' + created_at + '</span></p>' +
                    '        </div>' +
                    '    </div>' +
                    '</div>' +
                    '</a>';

            }
            $('#notification-container').empty();
            $('#notification-container').html(html);
        }
    });

    $.ajax({
        url: '/core/api/user_total_messages/',
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            html = '';
            
            var totals = response.results[0];
            
            // "total_messages": 55,
            // "total_messages_unread": 54,
            // "total_messages_trash": 0,
            // "total_messages_read": 1
            
            $('#total_nessage_tool_bar').empty();
            $('#total_nessage_tool_bar').html(totals.total_messages_unread);
            $('#total_nessage_unread').empty();
            $('#total_nessage_unread').html(totals.total_messages_unread);
            $('#total_nessage_menu').empty();
            $('#total_nessage_menu').html(totals.total_messages_unread);
        }
    });


}, 5000); // Check every 5 seconds



