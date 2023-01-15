function increaseCounter(counterId, increase) {
    fetch("/increase-counter", {
        method: 'POST',
        body: JSON.stringify({ counterId: counterId, increase: increase }),
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

function likeMovie(movieId, increase) {
    fetch("/like-movie", {
        method: 'POST',
        body: JSON.stringify({ movieId: movieId, increase: increase }),
    }).then((_res) => {
        window.location.href = "/movies";
    });
}