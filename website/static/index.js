function increaseCounter(counterId) {
    fetch("/increase-counter", {
        method: 'POST',
        body: JSON.stringify({ counterId: counterId }),
    }).then((_res) => {
        window.location.href = "/counter";
    });
}
