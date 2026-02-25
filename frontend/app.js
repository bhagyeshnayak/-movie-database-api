async function searchMovie() {

    const query = document.getElementById("search").value;

    const response = await fetch(
        `http://127.0.0.1:8000/api/v1/search/?q=${query}`
    );

    const data = await response.json();

    const container = document.getElementById("movies");
    container.innerHTML = "";

    data.results.forEach(movie => {

        container.innerHTML += `
            <div class="movie">
                <h3>${movie.title}</h3>
                <p>Rating: ${movie.vote_average}</p>
            </div>
        `;
    });
}