
// Updates like count for a given profile ID
function updatenumLikes(id, likes) {
    let likeCount = document.getElementById(`postlikecount_${id}`);
    likeCount.innerHTML = likes;
}

function finishEditing(id) {
    // Removes editing textbox, save and cancel
    document.getElementById(`textarea_${id}`).remove()
    document.getElementById(`save_${id}`).remove()
    document.getElementById(`cancel_${id}`).remove()

    // Show post and num likes 
    document.getElementById(`postcontent_${id}`).style.display = 'block';
    document.getElementById(`editpost_${id}`).style.display = 'inline-block';
    document.getElementById(`post_likes_${id}`).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {

    // Listens for clicks on page
    document.addEventListener('click', event => {
        
        // Saves element user clicked on
        const element = event.target;

        // If user clicks on a heart icon
        if (element.id.startsWith('heartbtn_')) {
        
            // Save post ID
            let id = element.dataset.id;
            console.log(id)
            
            // Make fetch request to update page dynamically
            fetch(`/updatelikecount/${id}`, {
                method: "POST"
            })
            .then(function(response) {
                if (response.ok) {
                    return response.json()
                }
                // returns an error to the console if json response fails.
                else {
                    return Promise.reject('Error')
                }
            }).then(function(data) {
                
                const likes = data.numLikes;
                const postLikes = data.postLikes;

                let heartIcon = document.getElementById(`heartbtn_${id}`);
                
                // span element of # of likes updates here
                updatenumLikes(id, likes)

                // updates heart to be filled or empty if user likes post
                if (postLikes) {
                    heartIcon.className = 'fa fa-heart';
                } else {
                    heartIcon.className = 'fa fa-heart-o';
                }
                
            })
            .catch(error => {
                console.error(error);
            })
        }

        if (element.id.startsWith('editpost_')) {
            console.log("inside edit post func")
            let id = element.dataset.id;
            console.log(id)
            let posttext = document.getElementById(`postcontent_${id}`)
            
            // create text area for editing post
            let textArea = document.createElement('textarea');
            textArea.innerHTML = posttext.innerHTML;
            textArea.id = `textarea_${id}`;
            textArea.className = 'form-control';
            document.getElementById(`postcontentgroup_${id}`).append(textArea);

            // Hide original post text
            posttext.style.display = 'none';

            // 'Cancel' button added to screen
            const cancelButton = document.createElement('button');
            cancelButton.innerHTML = 'Cancel';
            cancelButton.className = 'btn btn-danger btn-sm';
            cancelButton.id = `cancel_${id}`

            // 'Save' button added to screen
            const saveButton = document.createElement('button');
            saveButton.innerHTML = 'Save';
            saveButton.className = 'btn btn-primary btn-sm';
            saveButton.id = `save_${id}`

            // Add buttons to DOM
            document.getElementById(`savecancelbtns_${id}`).append(saveButton);
            document.getElementById(`savecancelbtns_${id}`).append(cancelButton);

            // Event listener for when user clicks 'Cancel' button
            cancelButton.addEventListener('click', function() {
                finishEditing(id)
            })

            // Event listener for when user clicks 'Save' button
            saveButton.addEventListener('click', function() {
                posttextArea = document.getElementById(`textarea_${id}`);

                fetch(`/editpost/${id}`, {
                    method: "POST",
                    body: JSON.stringify({
                        // Pass through the new content typed in the text area
                        content: posttextArea.value,
                    })
                })
                .then(function(response) {
                    if (response.ok) {
                        return response.json()
                    }
                    // returns an error to the console if json response fails.
                    else {
                        return Promise.reject('Error')
                    }
                })

                .then(result => {
                     if (!result.error) {
                    
                        // if successful, show new post with edits made
                        posttext.innerHTML = result.content;
                        
                        // Removes all editing functionality and returns to default
                        finishEditing(id)
                    } 
                    else {
                        finishEditing(id)
                    }
                })
                .catch(error => {
                    console.error(error);
                })
            })
            
        }
    })
})