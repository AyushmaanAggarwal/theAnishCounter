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


// Clock, directly from Stack Overflow

window.onload = displayClock();
function displayClock(){
  var display = new Date().toLocaleTimeString();
  document.getElementById("time").textContent = display
  setTimeout(displayClock, 1000); 
}