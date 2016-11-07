$(function(){

    $('#artist-search').submit(function(event){
        event.preventDefault();
        var searchUrl = 'https://api.spotify.com/v1/search';
        searchUrl += '?' + $.param({
            'q': $('#name').val(),
            'type': 'artist'
        });
        $.getJSON(searchUrl, function(data){
            console.log(data);
            if (data.artists.total === 0) {
                searchError("No results from search");
            }
            var artists = data.artists.items; // Extract artist array
            // Print all artists to browser window
            for (var i = 0; i < artists.length; i++){
                var $artistDiv = $('<li>', {id: i,
                                            'class': 'artist'});
                var addListener = function(id){
                    $artistDiv.click(function(){
                        createArtist(artists[id].id)
                    })
                }($artistDiv.attr('id')); //add current artist event listener
                $artistDiv.text(artists[i].name);
                $("#artists").append($artistDiv);
            }
        });
    });

});

// Flashes error message to user
// and allows manual creation of a music artist
function searchError(err){
    console.log('Error: ' + err);
}

function createArtist(spotifyId){
    $.ajax({
        type: 'POST',
        url: '/artist/create/',
        data: spotifyId
    })
}

// refresh with: window.location.reload(true)