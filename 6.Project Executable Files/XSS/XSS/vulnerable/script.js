document.getElementById("commentForm").addEventListener("submit", function(e) {
    e.preventDefault();
    
    let username = document.getElementById("username").value;
    let comment = document.getElementById("comment").value;

    if (!username || !comment) return;

    let commentBox = `<div class="comment-box"><strong>${username}:</strong> ${comment}</div>`;
    
    // 🚨 **XSS Vulnerability: Using innerHTML directly**
    document.getElementById("comments").innerHTML += commentBox;

    // Clear input fields
    document.getElementById("username").value = "";
    document.getElementById("comment").value = "";
});
