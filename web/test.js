const accordionItems = document.querySelectorAll('.accordion-item');

accordionItems.forEach(item => {
  const header = item.querySelector('.accordion-header');

  header.addEventListener('click', () => {
    // Check if this item is already active
    const isActive = item.classList.contains('active');

    // Close all accordion items first
    accordionItems.forEach(otherItem => {
      otherItem.classList.remove('active');
    });

    // If it wasn't active before, open it now
    if (!isActive) {
      item.classList.add('active');
    }
  });
});
