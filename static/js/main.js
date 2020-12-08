const btnDelete = document.querySelectorAll('.btn-delete')

function myFunction() {
    console.log(contactos);
}

if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm("Esta seguro de eliminar")) {
                e.preventDefault();
            }
        });
    });
}