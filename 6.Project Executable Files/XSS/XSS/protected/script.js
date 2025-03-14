document.getElementById("commentForm").addEventListener("submit", function(e) {
    e.preventDefault();
    
    let username = document.getElementById("username").value;
    let comment = document.getElementById("comment").value;

    if (!username || !comment) return;

    // Escape HTML to prevent XSS
    function escapeHTML(str) {
        return str.replace(/&/g, "&amp;")
                  .replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;")
                  .replace(/"/g, "&quot;")
                  .replace(/'/g, "&#039;");
    }

    let safeUsername = escapeHTML(username);
    let safeComment = escapeHTML(comment);

    let commentBox = `<div class="comment-box"><strong>${safeUsername}:</strong> ${safeComment}</div>`;
    
    // ✅ **Safe insertion using sanitized input**
    document.getElementById("comments").innerHTML += commentBox;

    // Clear input fields
    document.getElementById("username").value = "";
    document.getElementById("comment").value = "";
});
