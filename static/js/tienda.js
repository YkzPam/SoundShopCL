// JavaScript directo: disponible al descargar el repositorio, sin compilar.
const raiz = document.documentElement;
const botonTema = document.getElementById('cambiar-tema');
function aplicarTema(tema) {
  raiz.dataset.bsTheme = tema;
  botonTema?.setAttribute('aria-label', tema === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
}
try { aplicarTema(localStorage.getItem('soundshop-tema') || 'light'); } catch (_) { aplicarTema('light'); }
botonTema?.addEventListener('click', () => {
  const tema = raiz.dataset.bsTheme === 'dark' ? 'light' : 'dark';
  aplicarTema(tema);
  try { localStorage.setItem('soundshop-tema', tema); } catch (_) { /* El tema funciona sin almacenamiento. */ }
});
document.querySelectorAll('.navbar-nav a').forEach(enlace => {
  if (new URL(enlace.href).pathname === location.pathname) enlace.setAttribute('aria-current', 'page');
});
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observador = new IntersectionObserver(entradas => {
    entradas.forEach(entrada => {
      if (entrada.isIntersecting) {
        entrada.target.classList.remove('pendiente');
        observador.unobserve(entrada.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(elemento => {
    elemento.classList.add('pendiente');
    observador.observe(elemento);
  });
}
