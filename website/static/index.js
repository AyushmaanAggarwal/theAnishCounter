function increaseCounter(counterId) {
    fetch("/increase-counter", {
        method: 'POST',
        body: JSON.stringify({ counterId: counterId }),
    }).then((_res) => {
        window.location.href = "/counter";
    });
}

function deleteCounter(counterId) {
    fetch("/delete-counter", {
        method: 'POST',
        body: JSON.stringify({ counterId: counterId }),
    }).then((_res) => {
        window.location.href = "/counter";
    });
}

function likeMovie(movieId) {
    fetch("/like-movie", {
        method: 'POST',
        body: JSON.stringify({ movieId: movieId }),
    }).then((_res) => {
        window.location.href = "/movies";
    });
}
function unlikeMovie(movieId) {
    fetch("/unlike-movie", {
        method: 'POST',
        body: JSON.stringify({ movieId: movieId }),
    }).then((_res) => {
        window.location.href = "/movies";
    });
}