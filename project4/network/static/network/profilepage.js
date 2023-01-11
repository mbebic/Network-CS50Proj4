// Updates fol/unfol status for a given profile ID
function updateFolUnfol(followbyval, followingval, btnflag, id) {
    let flwrCount = document.getElementById('fwlrcount'); 
    let flwingcount = document.getElementById('flwingcount');
    flwrCount.innerHTML = followbyval + ' Followers';
    flwingcount.innerHTML = followingval + ' Following';

    if (btnflag == 'Following') {
        let flwbtn = document.getElementById(`folunfolbutton_${id}`);
        flwbtn.innerHTML="Unfollow";
    }
    else {
        let flwbtn = document.getElementById(`folunfolbutton_${id}`);
        flwbtn.innerHTML="Follow";
    }

}

document.addEventListener('DOMContentLoaded', function() {
    // Listens for any clicks on the page
    document.addEventListener('click', event => {
        
        // Saves element user clicked on
        const element = event.target;

        // If user clicks on a heart icon
        if (element.id.startsWith('folunfolbutton')) {
            console.log("found the follow button")
            // Save username ID
            let id = element.dataset.id;
            let username = document.getElementById("userprofile").innerHTML;
            console.log("id, username:")
            console.log(id)
            console.log(username)

            
            // Make fetch request to update page dynamically
            fetch(`/followunfollow/${id}`, {
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
                console.log("json response has been returned")
                console.log(data)
                const followbyval = data.followed_by;
                const followingval = data.following;
                const btnflag = data.buttonflag;
                // const likes = data.numLikes;
                // const postLikes = data.postLikes;

                // let likeIcon = document.getElementById(`hearticon_${id}`);
                
                // // span element of # of likes updates here
                updateFolUnfol(followbyval, followingval, btnflag, id)

                // // updates heart to be filled or empty if user likes post
                // if (postLikes) {
                //     likeIcon.className = 'fa fa-heart';
                // } else {
                //     likeIcon.className = 'fa fa-heart-o';
                // }
                
            }).catch(function(ex) {
                console.log("parsing failed", ex);
            });
        }

        
    })
})