document.addEventListener('DOMContentLoaded', function() {
    checkAuthState();
    loadUserReviews();
});

async function loadUserReviews() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch('/api/user/reviews', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else if (response.status === 401) {
            // Unauthorized - redirect to home
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviewsList');
    const noReviews = document.getElementById('noReviews');

    if (!reviews || reviews.length === 0) {
        noReviews.style.display = 'block';
        reviewsList.innerHTML = '';
        return;
    }

    noReviews.style.display = 'none';
    reviewsList.innerHTML = reviews.map(review => `
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${review.movie.title}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${review.movie.director} (${review.movie.year})</h6>
                    <div class="mb-2">
                        ${review.movie.genres.map(genre => 
                            `<span class="badge bg-primary me-1">${genre}</span>`
                        ).join('')}
                    </div>
                    <p class="card-text">Your rating: ${review.rating}/5</p>
                    <p class="card-text">${review.comment || 'No comment provided'}</p>
                    <p class="card-text"><small class="text-muted">Reviewed on ${new Date(review.created_at).toLocaleDateString()}</small></p>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadYourMovies() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/your-movies/list', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const movies = await response.json();
        displayMovies(movies);
    } catch (error) {
        console.error('Error loading your movies:', error);
        document.getElementById('movieList').innerHTML = 
            `<div class="alert alert-danger">Error loading your movies: ${error.message}</div>`;
    }
}

function displayMovies(movies) {
    const movieList = document.getElementById('movieList');
    if (!movies.length) {
        movieList.innerHTML = '<div class="alert alert-info">You haven\'t rated any movies yet.</div>';
        return;
    }

    movieList.innerHTML = movies.map(movie => `
        <div class="movie-card" onclick="location.href='/movie/${movie.id}'">
            <h3 class="h5 mb-3">${movie.title}</h3>
            <p class="mb-2">
                <strong>Your Rating:</strong><br>
                ${'⭐'.repeat(movie.your_rating)}
            </p>
            <p class="mb-2">
                <strong>Director:</strong><br>
                ${movie.director}
            </p>
            <p class="mb-0">
                <strong>Genres:</strong><br>
                ${movie.genres.join(', ')}
            </p>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
        document.getElementById('userEmail').textContent = userEmail;
    }

    loadYourMovies();

    document.getElementById('logoutBtn')?.addEventListener('click', () => {
        localStorage.removeItem('token');
        localStorage.removeItem('userEmail');
        window.location.href = '/login';
    });
}); 