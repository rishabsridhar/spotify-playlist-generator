$(document).ready(function() {
            
    $('#get_reddit_songs').click(function() {
        console.log('get was clicked')
        $.ajax({
            url: "/_get_reddit_songs",
            type: "POST",
            datatype: 'json',
            data: JSON.stringify({
                'spotify_username': $('#spotify_username').val(),
                'playlist_name': $('#playlist_name').val()
            }),
            success: function (response) {
                console.log('success!')
                document.write(response)
            },
            error: function (xhr) {
                console.log('ERROR')
                console.log(xhr)
            }
        });
    });
})

$(document).on('click', '#add_reddit_songs', function() {
    console.log('add was clicked')
    $('#added_songs').html('Songs added! Redirecting to homepage...')
    $('.reddit_songs').html('')
    $.ajax({
        url: "/_add_reddit_songs",
        type: "POST",
        datatype: 'json',
        data: JSON.stringify({
            'spotify_username': $('#spotify_username').val(),
            'playlist_name': $('#playlist_name').val()
        }),
        success: function (response) {
            console.log('success! Songs added!')
            window.location.href = 'http://localhost:5000/'
        },
        error: function (xhr) {
            console.log('ERROR')
            console.log(xhr)
        }
    });
});