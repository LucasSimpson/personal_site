

// $(document).ready
document.addEventListener("DOMContentLoaded", function() {

    console.log("DOM Loaded");

    document.getElementById('burger-icon').addEventListener('click', function() {
        var side_nav = document.getElementById('side-nav');

        if (side_nav.classList.contains('show-nav')) {
            side_nav.classList.remove('show-nav');
        } else {
            side_nav.classList.add('show-nav');
        }
    });

});



