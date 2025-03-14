// Get movie ID from URL
const movieId = window.location.pathname.split('/').pop();

document.addEventListener('DOMContentLoaded', function() {
    loadMovieDetails();
    loadReviews();
    
    // Add submit event listener to the form
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', submitReview);
    }
});

function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        // Save current URL to return after login
        const currentPage = window.location.pathname;
        window.location.href = `/login?returnUrl=${encodeURIComponent(currentPage)}`;
        return false;
    }
    return token;
}

async function submitReview(event) {
    event.preventDefault();
    
    // Get the token
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // Get form data
    const rating = document.querySelector('select[name="rating"]').value;
    const comment = document.querySelector('textarea[name="comment"]').value;
    const movieId = window.location.pathname.split('/').pop();

    try {
        const response = await fetch(`/api/movies/${movieId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                rating: parseInt(rating),
                comment: comment
            })
        });

        if (response.status === 401) {
            // Token might be expired
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }

        if (!response.ok) {
            throw new Error('Failed to submit review');
        }

        // Clear form and reload reviews
        document.querySelector('select[name="rating"]').value = '1';
        document.querySelector('textarea[name="comment"]').value = '';
        
        // Reload reviews
        await loadReviews();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit review. Please try again.');
    }
}

async function loadMovieDetails() {
    try {
        const response = await fetch(`/api/movies/${movieId}`);
        if (!response.ok) {
            throw new Error('Failed to load movie details');
        }
        const movie = await response.json();
        displayMovieDetails(movie);
    } catch (error) {
        console.error('Error loading movie details:', error);
    }
}

async function loadReviews() {
    const movieId = window.location.pathname.split('/').pop();
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`/api/movies/${movieId}/reviews`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error('Failed to load reviews');
        
        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

function displayMovieDetails(movie) {
    // Add code to display movie details if needed
    console.log('Movie details:', movie);
}

function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews');
    if (!reviews.length) {
        reviewsContainer.innerHTML = '<p>No reviews yet</p>';
        return;
    }

    reviewsContainer.innerHTML = reviews.map(review => `
        <div class="review-card mb-3">
            <div class="card">
                <div class="card-body">
                    <h6 class="card-subtitle mb-2 text-muted">
                        By ${review.user_username} • Rating: ${'⭐'.repeat(review.rating)}
                    </h6>
                    <p class="card-text">${review.comment}</p>
                    <small class="text-muted">
                        ${new Date(review.created_at).toLocaleDateString()}
                    </small>
                </div>
            </div>
        </div>
    `).join('');
} 