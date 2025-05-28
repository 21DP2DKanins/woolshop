// shop/static/shop/js/cart.js

const CART_KEY = 'woolstore_cart';

function getCart() {
  return JSON.parse(localStorage.getItem(CART_KEY) || '{}');
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

/**
 * Добавить в корзину одну единицу товара с данным id
 */
export function addToCart(productId) {
  const cart = getCart();
  cart[productId] = (cart[productId] || 0) + 1;
  saveCart(cart);
  updateCartCounter();
  alert(`Добавлен товар #${productId}. В корзине: ${cart[productId]}`);
}

/**
 * Перерисовать счётчик корзины в шапке
 */
export function updateCartCounter() {
  const cart = getCart();
  const totalCount = Object.values(cart).reduce((sum, q) => sum + q, 0);
  const badge = document.querySelector('#cart-counter');
  if (badge) badge.textContent = totalCount;
}

/**
 * Отрисовать страницу корзины: список товаров, кол-во и сумму
 */
export async function renderCart() {
  const cart = getCart();
  const container = document.querySelector('#cart-container');
  container.innerHTML = '';
  if (Object.keys(cart).length === 0) {
    container.innerHTML = '<p>Корзина пуста.</p>';
    return;
  }

  let total = 0;
  for (let id of Object.keys(cart)) {
    const qty = cart[id];
    // Получаем детали товара из API (или встраиваем в шаблон JSON-список)
    const resp = await fetch(`/api/products/${id}/`);
    if (!resp.ok) continue;
    const p = await resp.json();
    const itemTotal = p.price * qty;
    total += itemTotal;

    const el = document.createElement('div');
    el.className = 'cart-item';
    el.innerHTML = `
      <h4>${p.name}</h4>
      <p>₽${p.price} × 
         <input type="number" min="0" value="${qty}" data-id="${id}" class="cart-qty"/>
         = ₽${itemTotal.toFixed(2)}
      </p>
      <button data-remove="${id}">Удалить</button>
    `;
    container.append(el);
  }
  const totalEl = document.createElement('p');
  totalEl.innerHTML = `<strong>Итого: ₽${total.toFixed(2)}</strong>`;
  container.append(totalEl);

  // Навешиваем обработчики
  container.querySelectorAll('.cart-qty').forEach(input => {
    input.addEventListener('change', ev => {
      const id = ev.target.dataset.id;
      const newQty = parseInt(ev.target.value) || 0;
      const cart = getCart();
      if (newQty > 0) cart[id] = newQty;
      else delete cart[id];
      saveCart(cart);
      updateCartCounter();
      renderCart();
    });
  });
  container.querySelectorAll('[data-remove]').forEach(btn => {
    btn.addEventListener('click', ev => {
      const id = ev.target.dataset.remove;
      const cart = getCart();
      delete cart[id];
      saveCart(cart);
      updateCartCounter();
      renderCart();
    });
  });
}

// Инициализация: ставим слушатели на кнопки и обновляем счётчик
document.addEventListener('DOMContentLoaded', () => {
  // кнопки «В корзину»
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      addToCart(btn.dataset.id);
    });
  });
  // шапка
  updateCartCounter();

  // если мы на странице /cart/, рисуем её
  if (window.location.pathname === '/cart/') {
    renderCart();
  }
});
