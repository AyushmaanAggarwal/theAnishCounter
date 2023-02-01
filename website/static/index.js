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

function addMovie(movieList) {
    fetch("/add-movie", {
        method: 'POST',
        body: JSON.stringify({ movie: movieList }),
    }).then((_res) => {
        window.location.href = "/movies";
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

function addBook(bookList) {
    fetch("/add-book", {
        method: 'POST',
        body: JSON.stringify({ book: bookList }),
    }).then((_res) => {
        window.location.href = "/books";
    });
}

function likeBook(bookId, increase) {
    fetch("/like-book", {
        method: 'POST',
        body: JSON.stringify({ bookId: bookId, increase: increase }),
    }).then((_res) => {
        window.location.href = "/books";
    });
}

function markHere(latenessId, here) {
    fetch("/mark-here", {
        method: 'POST',
        body: JSON.stringify({ latenessId: latenessId, here: here }),
    }).then((_res) => {
        window.location.href = "/lateness-tracker";
    });
}