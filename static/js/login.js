$(function(){
    $('#sign-out').click(signOut);
    function signOut() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
            console.log('User signed out.');
        });
    }
});

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail());
    id_token = googleUser.getAuthResponse().id_token;
    auth_data = {
        'token': id_token,
        'state': '{{STATE}}'
    }
    $.ajax({
        url: '/gconnect',
        method: 'POST',
        data: auth_data,
        success: function(){
            console.log('token sent')
        }
    });
}