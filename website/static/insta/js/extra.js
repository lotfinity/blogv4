document.addEventListener("DOMContentLoaded", function () {
    var swiper = new Swiper('.swiper-container', {
        slidesPerView: '5',
        spaceBetween: 2,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    let page = 1;  // Start from page 1 for the additional posts
    let loading = false;
    let postContainer = document.getElementById("posts_sec");

    function lazyLoadImages() {
        document.querySelectorAll(".lazy-load").forEach(img => {
            if (img.getAttribute("data-src") && img.getBoundingClientRect().top < window.innerHeight) {
                img.src = img.getAttribute("data-src");
                img.removeAttribute("data-src");
            }
        });
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('.lazy-load').forEach(img => {
        observer.observe(img);
    });

    function loadMorePosts() {
        if (loading) return;
        loading = true;

        fetch(window.location.href + "?page=" + page, {
            headers: { "X-Requested-With": "XMLHttpRequest" }  // Important for detecting AJAX requests
        })
        .then(response => response.json())
        .then(data => {
            if (data.posts.length === 0) return;  // No more posts

            data.posts.forEach(post => {
                let item = document.createElement("div");
                item.classList.add("item");

                if (post.image) {
                    let img = document.createElement("img");
                    img.classList.add("img-fluid", "item_img", "lazy-load");
                    img.setAttribute("data-src", post.image);
                    item.appendChild(img);
                } else if (post.video) {
                    let video = document.createElement("video");
                    video.classList.add("img-fluid", "item_img");
                    video.setAttribute("controls", "true");
                    let source = document.createElement("source");
                    source.setAttribute("src", post.video);
                    source.setAttribute("type", "video/mp4");
                    video.appendChild(source);
                    item.appendChild(video);
                }

                postContainer.appendChild(item);
            });

            page++;
            loading = false;
            lazyLoadImages();  // Trigger lazy loading after adding new posts
        })
        .catch(() => loading = false);
    }

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !loading) {
                loadMorePosts();
            }
        });
    }, { threshold: 0.1 });

    // Observe a sentinel element at bottom
    const sentinel = document.createElement('div');
    document.body.appendChild(sentinel);
    scrollObserver.observe(sentinel);

    lazyLoadImages();  // Ensure images load on initial page load

    const toggle = document.getElementById('dark-mode-toggle');
    const body = document.body;
    const darkModeKey = "dark-mode-enabled";

    // Check localStorage for dark mode preference
    if (localStorage.getItem(darkModeKey) === "true") {
        body.classList.add('dark-mode');
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            body.classList.toggle('dark-mode');

            // Save preference in localStorage
            if (body.classList.contains('dark-mode')) {
                localStorage.setItem(darkModeKey, "true");
            } else {
                localStorage.setItem(darkModeKey, "false");
            }
        });
    } else {
        console.warn("Dark mode toggle button not found.");
    }

    // Dark Mode System Preference Detection
    function updateDarkMode() {
        const isSystemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const userPrefersDark = localStorage.getItem("dark-mode-enabled") === "true";
        const body = document.body;

        if (localStorage.getItem("dark-mode-enabled") === null) {
            // First visit - follow system preference
            if (isSystemDark) {
                body.classList.add('dark-mode');
                localStorage.setItem(darkModeKey, "true");
            }
        } else {
            // Subsequent visits - follow user preference
            body.classList.toggle('dark-mode', userPrefersDark);
        }
    }

    // Initialize on page load
    updateDarkMode();

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (localStorage.getItem("dark-mode-enabled") === null) {
            updateDarkMode();
        }
    });
});

