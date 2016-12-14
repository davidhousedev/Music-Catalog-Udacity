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
            $("#artists").text(''); // Clear any existing search results
            // Print all artists to browser window
            for (var i = 0; i < artists.length; i++){
                var $artistDiv = $('<div>', {id: i,
                                            'class': 'artist row'});
                var addListener = function(id){
                    $artistDiv.click(function(){
                        createArtist($(this),
                                     artists[id].id,
                                     artists[id].name)
                    })
                }($artistDiv.attr('id')); //add current artist event listener
                $artistDiv.text(artists[i].name);
                var $artistImg = $(document.createElement('img'));
                var imgUrl = artists[i].images.pop().url;
                $artistImg.attr('src', imgUrl);
                $artistImg.attr('class', 'artist-thumbnail float-xs-left');
                $artistDiv.append($artistImg);
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

function createArtist(element, spotifyId, name){
    element.hide();
    var status = $(document.createElement('div'));
    status.attr('id', spotifyId);
    status.css('display', 'block');
    console.log(status);
    status.text('Adding ' + name + '...');
    $('#artists-added').append(status);

    $.ajax({
        type: 'POST',
        url: '/artist/create/',
        data: spotifyId,
        error: function(){
            artistAddError(status, element);
        },
        success: function(data){
            json = JSON.parse(data)
            addingSuccessful(status, json, name);
        }
    });
}

// This function is called while an artist is being added to the database
// Displays a status message informing user that database is currently working
function addingArtist(element, name){
    console.log(element);
    element.append('Adding ' + name + '...');
}

function addingSuccessful(element, json, name){
    console.log(json);
    element.text('Successfully added ' + name);
    var artistLink = $(document.createElement('a'));
    artistLink.attr('href', json.artist_url);
    artistLink.append('View artist');
    console.log(artistLink)
    element.append('<br>');
    element.append(artistLink)
}

function artistAddError(status, searchResult){
    status.hide();
    searchResult.show();
    searchResult.append(' Unable to add');
}

// refresh with: window.location.reload(true)