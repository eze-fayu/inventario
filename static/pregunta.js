const btn_accion = document.querySelector('.boton-acc')

if(btn_accion) {
    const btnArray = Array.from(btn_accion);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if(!confirm('Seguro que quieres modificar?')) {
                e.preventDefault();
            }
        });
    });
}