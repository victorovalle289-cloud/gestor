// Declaración global de la URL base del backend Flask
const BASE_URL = "http://127.0.0.1:5000";

// Función para visualizar datos en la tabla (index.html)
function visualizar(data) {
    let tabla = "";
    if (data.baul && Array.isArray(data.baul)) {
        data.baul.forEach(item => {
            tabla += `
            <tr data-id="${item.id_baul}">
                <td>${item.id_baul}</td>
                <td>${item.Plataforma}</td>
                <td>${item.usuario}</td>
                <td>••••••••</td>
                <td>
                    <button type='button' class="btn btn-info" onclick="location.href='edit.html?variable1=${item.id_baul}'">
                        <img src='imagenes/edit.png' height='20' width='20'/>
                    </button>
                </td>
                <td>
                    <button type='button' class="btn btn-warning" onclick="eliminar(${item.id_baul})">
                        <img src='imagenes/delete.png' height='20' width='20'/>
                    </button>
                </td>
            </tr>`;
        });
    }
    const dataContainer = document.getElementById('data');
    if (dataContainer) {
        dataContainer.innerHTML = tabla;
    }
}

// Consulta general
function consulta_general() {
    fetch(`${BASE_URL}/`)
        .then(response => {
            if (!response.ok) throw new Error(`Error: ${response.status}`);
            return response.json();
        })
        .then(data => visualizar(data))
        .catch(error => console.error('Error:', error));
}

// Eliminar un registro
function eliminar(id) {
    fetch(`${BASE_URL}/eliminar/${id}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error(`Error: ${response.status}`);
            return response.json();
        })
        .then(res => {
            actualizarDOM(id);
            swal("Mensaje", `Registro ${res.mensaje} exitosamente`, "success");
        })
        .catch(error => console.error("Error:", error));
}

function actualizarDOM(id) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) row.remove();
}

// Guardar/Registrar nuevo
function registrar() {
    const plat = document.getElementById("plataforma").value;
    const usua = document.getElementById("usuario").value;
    const clav = document.getElementById("clave").value;

    if (!plat || !usua || !clav) {
        swal("Atención", "Por favor llena todos los campos", "warning");
        return;
    }

    const data = {
        plataforma: plat,
        usuario: usua,
        clave: clav
    };

    fetch(`${BASE_URL}/registro/`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return response.json();
    })
    .then(response => {
        if (response.mensaje === "Error") {
            swal("Mensaje", "Error en el registro", "error");
        } else {
            swal("Mensaje", "Registro agregado exitosamente", "success");
            setTimeout(() => { location.href = "index.html"; }, 1500);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Obtener datos individuales
function consulta_individual(id) {
    fetch(`${BASE_URL}/consulta_individual/${id}`)
        .then(response => {
            if (!response.ok) throw new Error(`Error: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.baul) {
                document.getElementById("plataforma").value = data.baul.Plataforma;
                document.getElementById("usuario").value = data.baul.usuario;
                document.getElementById("clave").value = "";
            }
        })
        .catch(error => console.error('Error:', error));
}

// Modificar datos
function modificar(id) {
    const plat = document.getElementById("plataforma").value;
    const usua = document.getElementById("usuario").value;
    const clav = document.getElementById("clave").value;

    if (!plat || !usua || !clav) {
        swal("Atención", "Por favor llena todos los campos", "warning");
        return;
    }

    const data = {
        plataforma: plat,
        usuario: usua,
        clave: clav
    };

    fetch(`${BASE_URL}/actualizar/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return response.json();
    })
    .then(response => {
        if (response.mensaje === "Error") {
            swal("Mensaje", "Error al actualizar el registro", "error");
        } else {
            swal("Mensaje", "Registro actualizado exitosamente", "success");
            setTimeout(() => { location.href = "index.html"; }, 1500);
        }
    })
    .catch(error => console.error('Error:', error));
}