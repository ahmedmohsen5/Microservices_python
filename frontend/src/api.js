export const getProducts = async () => {
    const response = await fetch('/api/products');
    return response.json();
  };
  
  export const getProduct = async (id) => {
    const response = await fetch(`/api/products/${id}`);
    return response.json();
  };
  
  export const login = async (username, password) => {
    const response = await fetch('/api/users/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  };
  
  export const register = async (username, email, password) => {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    });
    if (!response.ok) throw new Error('Registration failed');
    return response.json();
  };