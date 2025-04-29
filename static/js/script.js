const formTitle = document.getElementById('formTitle');
const toggleForm = document.getElementById('toggleForm');
const authForm = document.getElementById('authForm');

let isLogin = true;

toggleForm.addEventListener('click', () => {
  isLogin = !isLogin;
  formTitle.textContent = isLogin ? 'Login' : 'Register';
  toggleForm.textContent = isLogin ? "Don't have an account? Register" : "Already have an account? Login";
});

authForm.addEventListener('submit', (e) => {
    const userType = document.getElementById('userType').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    if (!userType) {
      alert('Please select a user type.');
      e.preventDefault();
      return;
    }
  
    if (isLogin) {
      authForm.action = '/login'; // set correct action
    } else {
      authForm.action = '/register'; // set correct action
    }
  
    authForm.method = 'POST'; // ensure method is POST
  
    // No need to e.preventDefault() here!
    // Let the form naturally submit after setting action/method.
  });
  