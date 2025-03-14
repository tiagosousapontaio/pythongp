console.log('JavaScript loaded');

// Debug flag
const DEBUG = true;

let searchTimeout = null;

// Authentication state management
let isLoggedIn = false;
let currentUserEmail = null;

// Fetch and display movies
async function loadMovies(search = '', genre = 'All Genres') {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(
            `/movies/?search=${encodeURIComponent(search)}&genre=${encodeURIComponent(genre)}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const movies = await response.json();
        displayMovies(movies);
    } catch (error) {
        console.error('Error loading movies:', error);
        document.getElementById('movieList').innerHTML = 
            `<div class="alert alert-danger">Error loading movies: ${error.message}</div>`;
    }
}

// Display movies in grid
function displayMovies(movies) {
    const movieList = document.getElementById('movieList');
    if (!movies.length) {
        movieList.innerHTML = '<div class="alert alert-info">No movies found</div>';
        return;
    }

    movieList.innerHTML = movies.map(movie => `
        <div class="movie-card" onclick="location.href='/movie/${movie.id}'">
            <h3 class="h5 mb-3">${movie.title}</h3>
            <p class="mb-2">
                <strong>Director:</strong><br>
                ${movie.director}
            </p>
            <p class="mb-2">
                <strong>Year:</strong><br>
                ${movie.year}
            </p>
            <p class="mb-0">
                <strong>Genres:</strong><br>
                ${movie.genres.join(', ')}
            </p>
        </div>
    `).join('');
}

// Search movies
async function searchMovies() {
    const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();
    const response = await fetch('/movies/');
    const movies = await response.json();
    
    if (searchTerm === '') {
        displayMovies(movies); // Show all movies if search is empty
        return;
    }

    const filteredMovies = movies.filter(movie => 
        movie.title.toLowerCase().includes(searchTerm) ||
        movie.director.toLowerCase().includes(searchTerm) ||
        movie.synopsis.toLowerCase().includes(searchTerm)
    );
    
    displayMovies(filteredMovies);
}

// Add movie function
async function addMovie() {
    const form = document.getElementById('addMovieForm');
    const formData = new FormData(form);
    
    const movieData = {
        title: formData.get('title'),
        director: formData.get('director'),
        year: parseInt(formData.get('year')),
        genre_ids: Array.from(document.getElementById('genres').selectedOptions).map(option => option.value),
        synopsis: formData.get('synopsis')
    };

    try {
        const response = await fetch('/movies/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(movieData)
        });

        if (response.ok) {
            // Show success message
            alert('Movie added successfully!');
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addMovieModal'));
            modal.hide();
            // Refresh movie list
            loadMovies();
            // Reset form
            form.reset();
        } else {
            alert('Error adding movie. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding movie. Please try again.');
    }
}

// Update the genre filter function
async function filterByGenre(genre) {
    try {
        console.log('Filtering by genre:', genre);
        const response = await fetch(genre ? `/movies/?genre=${genre}` : '/movies/');
        const movies = await response.json();
        console.log('Filtered movies:', movies);
        displayMovies(movies);
    } catch (error) {
        console.error('Error filtering movies:', error);
    }
}

// Authentication functions
async function login() {
    const form = document.getElementById('loginForm');
    const formData = new FormData(form);
    
    try {
        console.log('Attempting login...'); // Debug log
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': formData.get('email'),
                'password': formData.get('password')
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user_email', formData.get('email'));
            
            // Close modal
            const loginModal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
            loginModal.hide();
            
            // Update UI
            document.querySelector('.btn-outline-light').style.display = 'none';
            document.querySelector('.btn-primary').style.display = 'none';
            
            // Show user email and logout button
            const navbarRight = document.querySelector('.ms-auto');
            navbarRight.innerHTML = `
                <span class="navbar-text me-3">${formData.get('email')}</span>
                <button class="btn btn-outline-light" onclick="logout()">Logout</button>
            `;
            
            // Reload movies
            loadMovies();
        } else {
            alert(data.detail || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('username');
    location.reload();
}

function updateAuthUI(isLoggedIn, email = null) {
    const loggedOutButtons = document.getElementById('loggedOutButtons');
    const loggedInButtons = document.getElementById('loggedInButtons');
    const userEmailSpan = document.getElementById('userEmail');
    const yourMoviesLink = document.getElementById('yourMoviesLink');

    if (isLoggedIn && email) {
        loggedOutButtons.style.display = 'none';
        loggedInButtons.style.display = 'flex';
        userEmailSpan.textContent = email;
        yourMoviesLink.style.display = 'block';  // Show Your Movies link
    } else {
        loggedOutButtons.style.display = 'flex';
        loggedInButtons.style.display = 'none';
        userEmailSpan.textContent = '';
        yourMoviesLink.style.display = 'none';  // Hide Your Movies link
    }
}

// Check auth status on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // Display user email
    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
        document.getElementById('userEmail').textContent = userEmail;
    }

    // Load movies and genres
    loadMovies();
    loadGenres();

    updateAuthUI(!!token);
});

// Update event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Load movies when page loads
    loadMovies();

    // Handle search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const genre = document.getElementById('genreSelect').value;
            loadMovies(this.value, genre);
        }, 300));
    }

    // Handle genre selection
    const genreSelect = document.getElementById('genreSelect');
    if (genreSelect) {
        genreSelect.addEventListener('change', function() {
            const search = document.getElementById('searchInput').value;
            loadMovies(search, this.value);
        });
    }
});

async function loadUserDashboard() {
    if (!localStorage.getItem('token')) return;
    
    const token = localStorage.getItem('token');
    try {
        // Load profile
        const profileResponse = await fetch('/my-profile', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const profile = await profileResponse.json();
        
        document.getElementById('userProfileInfo').innerHTML = `
            <p><strong>Username:</strong> ${profile.username}</p>
            <p><strong>Reviews:</strong> ${profile.reviews_count}</p>
            <p><strong>Watchlist:</strong> ${profile.watchlist_count}</p>
        `;

        // Load reviews
        const reviewsResponse = await fetch('/my-reviews', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const reviews = await reviewsResponse.json();
        displayUserReviews(reviews);

        // Load watchlist
        const watchlistResponse = await fetch('/my-watchlist', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const watchlist = await watchlistResponse.json();
        displayUserWatchlist(watchlist);

        // Show dashboard
        document.getElementById('userDashboard').style.display = 'block';
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function displayUserReviews(reviews) {
    const container = document.getElementById('myReviews');
    container.innerHTML = reviews.map(review => `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${review.movie.title}</h5>
                <div class="rating">★ ${review.rating}</div>
                <p class="card-text">${review.text}</p>
                <small class="text-muted">Posted on ${new Date(review.created_at).toLocaleDateString()}</small>
            </div>
        </div>
    `).join('');
}

function displayUserWatchlist(movies) {
    const container = document.getElementById('myWatchlist');
    container.innerHTML = movies.map(movie => `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${movie.title}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${movie.director} (${movie.year})</h6>
                <p class="card-text">${movie.synopsis}</p>
                <button class="btn btn-danger btn-sm" onclick="removeFromWatchlist(${movie.id})">
                    Remove from Watchlist
                </button>
            </div>
        </div>
    `).join('');
}

// Add this to your existing login success handler
async function onLoginSuccess() {
    updateAuthUI(true);
    await loadUserDashboard();
}

// Add watchlist functionality to movie cards
function addMovieCardButtons(movieElement, movie) {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'mt-2';
    buttonContainer.innerHTML = `
        <button class="btn btn-primary btn-sm me-2" onclick="addToWatchlist(${movie.id})">
            Add to Watchlist
        </button>
        <button class="btn btn-success btn-sm" onclick="showReviewModal(${movie.id})">
            Write Review
        </button>
    `;
    movieElement.querySelector('.card-body').appendChild(buttonContainer);
}

// Add this to ensure Bootstrap's JavaScript is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    if (token) {
        document.querySelector('.btn-outline-light').style.display = 'none';
        document.querySelector('.btn-primary').style.display = 'none';
        
        const logoutBtn = document.createElement('button');
        logoutBtn.className = 'btn btn-outline-light';
        logoutBtn.textContent = 'Logout';
        logoutBtn.onclick = logout;
        document.querySelector('.ms-auto').appendChild(logoutBtn);
    }
});

async function register() {
    const form = document.getElementById('registerForm');
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: formData.get('username'),
                email: formData.get('email'),
                password: formData.get('password')
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Close register modal
            const registerModal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
            registerModal.hide();
            
            // Show success message
            alert('Account created successfully! Please log in.');
            
            // Open login modal
            const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
            loginModal.show();
        } else {
            alert(data.detail || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
    }
}

// Make sure movies load when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, calling loadMovies');
    loadMovies();
});

// Add this line at the bottom to verify the script is completely loaded
console.log('main.js finished loading');

// Add this function to populate genre dropdown
async function loadGenres() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/genres/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const genres = await response.json();
        
        const genreSelect = document.getElementById('genreFilter');
        genreSelect.innerHTML = '<option>All Genres</option>' +
            genres.map(genre => `<option value="${genre.name}">${genre.name}</option>`).join('');
    } catch (error) {
        console.error('Error loading genres:', error);
    }
}

// Make sure the event listener is properly set up
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing...');
    
    // Load genres first
    loadGenres().then(() => {
        // Then load movies
        loadMovies();
        
        // Add event listener for genre selection
        const genreSelect = document.getElementById('genreSelect');
        if (genreSelect) {
            genreSelect.addEventListener('change', (event) => {
                console.log('Genre selected:', event.target.value);
                loadMovies(event.target.value);
            });
        }
    });
});

function handleSearch(event) {
    const searchTerm = event.target.value;
    const selectedGenre = document.getElementById('genreSelect').value;
    
    // Clear existing timeout
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // Set new timeout to avoid too many requests
    searchTimeout = setTimeout(() => {
        loadMovies(selectedGenre, searchTerm);
    }, 300);
}

// Modal handling functions
function showLoginModal() {
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    loginModal.show();
}

function showRegisterModal() {
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    registerModal.show();
}

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing modals');
    
    // Initialize all modals
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        new bootstrap.Modal(modal);
    });

    // Login form handler
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        try {
            const response = await fetch('/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('userEmail', email);
                localStorage.setItem('username', email.split('@')[0]);
                updateAuthUI(true, email);
                const loginModal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
                loginModal.hide();
                window.location.href = '/movies';
            } else {
                const errorDiv = document.getElementById('loginError');
                errorDiv.textContent = 'Invalid email or password';
                errorDiv.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    });

    // Register form handler
    document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        
        try {
            console.log('Attempting to register user:', email);
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Registration successful');
                // Try to login automatically
                const loginResponse = await fetch('/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
                });

                if (loginResponse.ok) {
                    const loginData = await loginResponse.json();
                    localStorage.setItem('token', loginData.access_token);
                    localStorage.setItem('userEmail', email);
                    localStorage.setItem('username', email.split('@')[0]);
                    updateAuthUI(true, email);
                    window.location.href = '/movies';
                }
            } else {
                console.error('Registration failed:', data);
                const errorDiv = document.getElementById('registerError');
                errorDiv.textContent = data.detail || 'Registration failed. Please try again.';
                errorDiv.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Registration error:', error);
            const errorDiv = document.getElementById('registerError');
            errorDiv.textContent = 'An error occurred during registration.';
            errorDiv.classList.remove('d-none');
        }
    });
});

// Keep your existing authentication state management code...

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    console.log('Login attempt starting...');

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');

    try {
        const formData = new FormData();
        formData.append('username', email);  // Note: FastAPI expects 'username', not 'email'
        formData.append('password', password);

        const response = await fetch('/token', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        // Store token
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('userEmail', email);
        localStorage.setItem('username', email.split('@')[0]);

        // Update UI
        const authButtons = document.getElementById('authButtons');
        const userInfo = document.getElementById('userInfo');
        
        if (authButtons && userInfo) {
            authButtons.style.display = 'none';
            userInfo.style.display = 'flex';
            const usernameSpan = userInfo.querySelector('.username');
            if (usernameSpan) {
                usernameSpan.textContent = email;
            }
        }

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
        if (modal) {
            modal.hide();
        }

        // Clear form
        event.target.reset();
        if (errorDiv) {
            errorDiv.textContent = '';
        }

        console.log('Login successful');
        window.location.href = '/movies'; // Refresh the page to update the UI

    } catch (error) {
        console.error('Login error:', error);
        if (errorDiv) {
            errorDiv.textContent = error.message;
        }
    }
}

// Handle logout
function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('username');
    window.location.href = '/login';
}

// Check login status on page load
function checkLoginStatus() {
    const token = localStorage.getItem('token');
    const userEmail = localStorage.getItem('userEmail');
    const authButtons = document.getElementById('authButtons');
    const userInfo = document.getElementById('userInfo');

    if (token && userEmail && authButtons && userInfo) {
        authButtons.style.display = 'none';
        userInfo.style.display = 'flex';
        const usernameSpan = userInfo.querySelector('.username');
        if (usernameSpan) {
            usernameSpan.textContent = userEmail;
        }
    }
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing...');
    
    // Check login status
    checkLoginStatus();
    
    // Load initial data
    loadMovies();
    loadGenres();
});

// Show registration modal
function showRegisterModal() {
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    registerModal.show();
}

// Handle registration
async function handleRegister(event) {
    event.preventDefault();
    console.log('Registration attempt...');

    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const errorDiv = document.getElementById('registerError');

    try {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);

        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed');
        }

        // Clear form and error message
        event.target.reset();
        errorDiv.textContent = '';

        // Show success message
        errorDiv.className = 'text-success';
        errorDiv.textContent = 'Registration successful! You can now log in.';

        // Close modal after 2 seconds
        setTimeout(() => {
            const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
            modal.hide();
            // Show login modal
            showLoginModal();
        }, 2000);

    } catch (error) {
        console.error('Registration error:', error);
        errorDiv.className = 'text-danger';
        errorDiv.textContent = error.message;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');
});

// Check login status on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking auth state');
    checkAuthState();
});

function checkAuthState() {
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('userEmail');
    
    if (token && email) {
        console.log('User is logged in:', email);
        updateAuthUI(true, email);
    } else {
        console.log('User is not logged in');
        updateAuthUI(false);
    }
}

function handleLogout() {
    console.log('Logging out');
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('username');
    updateAuthUI(false);
    window.location.href = '/login';
}

// Add these functions if you haven't already
function showLoginModal() {
    // Your existing login modal code
    console.log('Show login modal');
}

function showRegisterModal() {
    // Your existing register modal code
    console.log('Show register modal');
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check authentication on page load
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    if (!checkAuth()) return;
    
    loadMovies();
    loadGenres();

    const userEmail = localStorage.getItem('userEmail');
    if (userEmail) {
        document.getElementById('userEmail').textContent = userEmail;
    }

    const searchInput = document.querySelector('input[type="search"]');
    const genreFilter = document.getElementById('genreFilter');

    searchInput?.addEventListener('input', debounce(() => {
        loadMovies(searchInput.value, genreFilter.value);
    }, 300));

    genreFilter?.addEventListener('change', () => {
        loadMovies(searchInput?.value || '', genreFilter.value);
    });

    document.getElementById('logoutBtn')?.addEventListener('click', () => {
        localStorage.removeItem('token');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('username');
        window.location.href = '/login';
    });
});
