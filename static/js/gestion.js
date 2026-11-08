// La vista previa refleja el formulario. El guardado sigue a cargo de Django.
const formularioProducto = document.getElementById('producto-form');

if (formularioProducto) {
    const campoNombre = document.getElementById('nombre');
    const campoCodigo = document.getElementById('codigo');
    const campoDescripcion = document.getElementById('descripcion');
    const campoPrecio = document.getElementById('precio');
    const campoStock = document.getElementById('stock');
    const campoMarca = document.getElementById('marca');
    const campoCategoria = document.getElementById('categoria');
    const campoImagen = document.getElementById('imagen');
    const campoActivo = document.getElementById('activo');
    const foto = document.getElementById('vista-imagen');
    const sinImagen = document.getElementById('vista-sin-imagen');
    const mensajeImagen = document.getElementById('vista-imagen-mensaje');
    const formatoPrecio = new Intl.NumberFormat('es-CL', {
        maximumFractionDigits: 2
    });

    foto.addEventListener('load', () => {
        foto.hidden = false;
        sinImagen.hidden = true;
    });
    foto.addEventListener('error', () => {
        foto.hidden = true;
        sinImagen.hidden = false;
        mensajeImagen.textContent = 'Imagen no disponible';
    });

    function actualizarVistaProducto() {
        document.getElementById('vista-nombre').textContent = campoNombre.value.trim() ||
            'Nombre del producto';
        document.getElementById('vista-codigo').textContent = campoCodigo.value.trim() ||
            'Sin código';
        document.getElementById('vista-descripcion').textContent = campoDescripcion.value.trim() ||
            'La descripción del producto aparecerá aquí.';
        document.getElementById('vista-marca').textContent = campoMarca.value ? campoMarca
            .selectedOptions[0].textContent : 'Marca del equipo';
        document.getElementById('vista-categoria').textContent = campoCategoria.value ?
            campoCategoria.selectedOptions[0].textContent : 'Sin categoría';

        const precio = Number(campoPrecio.value);
        document.getElementById('vista-precio').textContent = campoPrecio.value && Number.isFinite(
            precio) && precio > 0 ? '$' + formatoPrecio.format(precio) : 'Precio por definir';
        const stock = Number(campoStock.value);
        const stockValido = campoStock.value !== '' && Number.isInteger(stock) && stock >= 0;
        document.getElementById('vista-stock').textContent = stockValido ? 'Stock: ' + stock :
            'Stock por definir';
        const estado = document.getElementById('vista-estado');
        estado.className = 'gestion-estado';
        if (!campoActivo.checked) {
            estado.textContent = 'Desactivado';
            estado.classList.add('estado-inactivo');
        } else if (!stockValido) {
            estado.textContent = 'Revisar stock';
            estado.classList.add('estado-bajo');
        } else if (stock === 0) {
            estado.textContent = 'Agotado';
            estado.classList.add('estado-agotado');
        } else if (stock < 5) {
            estado.textContent = 'Stock bajo';
            estado.classList.add('estado-bajo');
        } else {
            estado.textContent = 'Disponible';
        }

        const ruta = campoImagen.value.trim();
        if (foto.dataset.ruta !== ruta) {
            foto.dataset.ruta = ruta;
            foto.hidden = true;
            sinImagen.hidden = false;
            // Se muestran archivos locales de la tienda, no direcciones externas.
            if (ruta && !ruta.includes('..') && !ruta.includes(':') && !ruta.includes('\\') && !ruta
                .startsWith('/')) {
                mensajeImagen.textContent = 'Cargando imagen';
                foto.src = formularioProducto.dataset.staticUrl + ruta.split('/').map(
                    encodeURIComponent).join('/');
            } else {
                foto.removeAttribute('src');
                mensajeImagen.textContent = ruta ? 'Revisar el archivo de imagen' : 'Sin imagen';
            }
        }
    }

    formularioProducto.addEventListener('input', actualizarVistaProducto);
    formularioProducto.addEventListener('change', actualizarVistaProducto);
    actualizarVistaProducto();
}

const imprimirVenta = document.getElementById('imprimir-venta');
if (imprimirVenta) {
    imprimirVenta.addEventListener('click', () => window.print());
}
