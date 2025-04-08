document.addEventListener("DOMContentLoaded", function () {
    populateYearFilter();
    document.getElementById("recommend-btn").addEventListener("click", getRecommendations);
});

function getRecommendations() {
    const movieName = document.getElementById("movie-input").value.trim();
    const genre = document.getElementById("genre-filter").value;
    const year = document.getElementById("year-filter").value;
    const rating = document.getElementById("rating-filter").value;

    if (!movieName) {
        alert("Please enter a movie name.");
        return;
    }

    let url = `/recommend?movie=${encodeURIComponent(movieName)}`;
    if (genre) url += `&genre=${encodeURIComponent(genre)}`;
    if (year) url += `&year=${encodeURIComponent(year)}`;
    if (rating) url += `&rating=${encodeURIComponent(rating)}`;

    const moviesDiv = document.getElementById("movies");
    moviesDiv.innerHTML = '<div class="loader"></div>';

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayRecommendations(data);
        })
        .catch(error => {
            console.error("Error fetching recommendations:", error);
            moviesDiv.innerHTML = "<p>Error fetching recommendations. Please try again.</p>";
        });
}

function displayRecommendations(movies) {
    const moviesDiv = document.getElementById("movies");
    moviesDiv.innerHTML = "";

    movies.forEach(movie => {
        let movieElement = document.createElement("div");
        movieElement.classList.add("movie-card");

        let posterUrl = movie.poster_path ? movie.poster_path : "static/image-placeholder.jpg";

        movieElement.innerHTML = `
            <img src="${posterUrl}" alt="${movie.title}">
            <h3>${movie.title}</h3>
            <p><strong>Genre:</strong> ${movie.genre}</p>
            <p><strong>Rating:</strong> ⭐ ${movie.vote_average}</p>
        `;

        moviesDiv.appendChild(movieElement);
    });
}

function populateYearFilter() {
    const yearFilter = document.getElementById("year-filter");
    for (let year = 2025; year >= 1980; year--) {
        let option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    }
}
