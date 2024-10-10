import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import ProductList from './components/ProductList';
import ProductDetails from './components/ProductDetails';
import Cart from './components/Cart';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  const [cart, setCart] = useState([]);
  const [user, setUser] = useState(null);

  const addToCart = (product) => {
    setCart([...cart, product]);
  };

  return (
    <Router>
      <div className="App">
        <Header cartCount={cart.length} user={user} />
        <Switch>
          <Route exact path="/" component={ProductList} />
          <Route 
            path="/product/:id" 
            render={(props) => <ProductDetails {...props} addToCart={addToCart} />} 
          />
          <Route 
            path="/cart" 
            render={(props) => <Cart {...props} cart={cart} setCart={setCart} />} 
          />
          <Route 
            path="/login" 
            render={(props) => <Login {...props} setUser={setUser} />} 
          />
          <Route path="/register" component={Register} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;