document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.add-to-cart').forEach(btn => {
      btn.addEventListener('click', () => {
        alert(`Товар #${btn.dataset.id} добавлен в корзину (демо).`);
      });
    });
  });
  