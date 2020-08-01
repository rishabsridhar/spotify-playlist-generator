//$(document).ready(function(){

    $('#generate_playlist').click(function() {
        console.log('get was clicked')
        $('.generated_songs').html('')
        $.ajax({
            url: "/_get_playlist",
            type: "POST",
            datatype: 'json',
            data: JSON.stringify({
                'spotify_username': $('#spotify_username').val(),
                'playlist_name': $('#playlist_name').val(),
                'raw_artists': $('#artists').val(),
                'raw_tracks': $('#tracks').val(),
                'raw_genres': $('#genres').val()
            }),
            success: function (response) {
                console.log('success! data sent to backend.')
                document.write(response)
            },
            error: function (xhr) {
                console.log('ERROR')
                console.log(xhr)
            }
        });
    });
//})

$(document).on('click', '#add_songs', function() {
    console.log('add was clicked')
    $('.generated_songs').html('')
    $('#songs_are_added').html('Songs added! Redirecting to homepage...')
    $.ajax({
        url: "/_add_songs",
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