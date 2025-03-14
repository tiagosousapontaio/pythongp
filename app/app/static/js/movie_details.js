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
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    const rating = document.querySelector('select[name="rating"]').value;
    const comment = document.querySelector('textarea[name="comment"]').value;

    try {
        const movieId = window.location.pathname.split('/').pop();
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

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to submit review');
        }

        // Clear form and reload reviews
        document.querySelector('select[name="rating"]').value = '1';
        document.querySelector('textarea[name="comment"]').value = '';
        await loadReviews();

    } catch (error) {
        console.error('Error submitting review:', error);
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
    try {
        const response = await fetch(`/api/movies/${movieId}/reviews`);
        if (!response.ok) {
            throw new Error('Failed to load reviews');
        }
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
    const reviewsContainer = document.querySelector('.Reviews');
    if (reviews.length === 0) {
        reviewsContainer.innerHTML = '<p>No reviews yet</p>';
        return;
    }

    const reviewsHtml = reviews.map(review => `
        <div class="review">
            <p>Rating: ${review.rating}/5</p>
            <p>${review.comment || ''}</p>
            <small>Posted on: ${new Date(review.created_at).toLocaleDateString()}</small>
        </div>
    `).join('');

    reviewsContainer.innerHTML = reviewsHtml;
} 