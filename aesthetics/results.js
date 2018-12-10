if (document.getElementById('results-container').classList.contains('individual')) {
    firstContainer = document.getElementsByClassName('sub-breed')[0].classList.add('show-all');

    fetchMoreButtons = document.getElementsByClassName('fetch-more-button');
    for (let button of fetchMoreButtons) {
        button.addEventListener('click', function () {
            let breedContainer = document.querySelector('[data-breed="' + button.dataset.breed + '"]');
            breedContainer.classList.add('show-all')
        });
    }

    fetchLessButtons = document.getElementsByClassName('fetch-less-button');
    for (let button of fetchLessButtons) {
        button.addEventListener('click', function () {
            let breedContainer = document.querySelector('[data-breed="' + button.dataset.breed + '"]');
            breedContainer.classList.remove('show-all')
        });
    }
} else {
    fetchMoreButtons = document.getElementsByClassName('fetch-more-button');
    for (let button of fetchMoreButtons) {
        button.addEventListener('click', function () {
            window.location.href = '/picture-page?breed=' + button.dataset.breed;
        });
    }

    fetchLessButtons = document.getElementsByClassName('fetch-less-button');
    for (let button of fetchLessButtons) {
        button.addEventListener('click', function () {
            let breedContainer = document.querySelector('[data-breed="' + button.dataset.breed + '"]');
            breedContainer.classList.remove('show-all')
        });
    }
}