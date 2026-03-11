function openModal() {
  document.getElementById('modal-bg').style.display = 'flex';
}
function closeModal() {
  document.getElementById('modal-bg').style.display = 'none';
}
window.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('open-modal-btn');
  if (btn) btn.onclick = openModal;
  const closeBtn = document.getElementById('close-modal-btn');
  if (closeBtn) closeBtn.onclick = closeModal;
});
