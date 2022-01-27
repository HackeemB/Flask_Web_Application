//This function is going to take the note ID that we passed and its going to send a POST request 
// to the delete-note endpoint. Then, after is gets a response from this delete-note endpoint, 
// it's going to reload the window
function deleteNote(noteId) {
    // To send a request in vanilla-js, we use 'fetch'
    fetch('/delete-note', { 
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href = "/"; // This reloads the window
    });
}