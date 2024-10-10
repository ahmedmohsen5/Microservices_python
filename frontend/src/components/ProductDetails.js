import React, { useState, useEffect } from 'react';
import { getProduct } from '../api';

function ProductDetails({ match, addToCart }) {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    getProduct(match.params.id).then(setProduct);
  }, [match.params.id]);

  if (!product) return <div>Loading...</div>;

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
      <button onClick={() => addToCart(product)}>Add to Cart</button>
    </div>
  );
}

export default ProductDetails;