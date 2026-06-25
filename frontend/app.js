const API = "http://127.0.0.1:8000";

// -----------------------------
// LOGIN
// -----------------------------
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!data.access_token) {
            showAlert("alertLogin", "Credenciales incorrectas");
            return;
        }
        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "recetas.html";
        } else {
            alert("Credenciales incorrectas");
        }
    });
}

// -----------------------------
// REGISTRO
// -----------------------------
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const res = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        if (res.ok) {
            alert("Usuario creado");
            window.location.href = "index.html";
        } else {
            alert("Error al registrar");
        }
    });
}


// -----------------------------
// RECETAS
// -----------------------------
// Rellena el textarea con el texto del chip
function setPrompt(texto) {
    document.getElementById('mensaje').value = texto;
}

// Función principal mejorada: gestiona estado del botón, loading y llama a la API
async function generarReceta() {
    const mensaje = document.getElementById('mensaje').value.trim();
    const btn = document.getElementById('btnGenerar');
    const rightPanel = document.getElementById('rightPanel');

    if (!mensaje) {
        alert('Por favor, describe qué quieres cocinar.');
        return;
    }

    // Estado de carga
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Pensando receta...';
    rightPanel.innerHTML = `
        <div class="d-flex justify-content-center align-items-center h-100">
            <div class="text-center">
                <div class="spinner-border mb-3" role="status"></div>
                <p class="text-muted">El chef IA está preparando tu receta...</p>
            </div>
        </div>`;

    try {
        const response = await fetch(`${API}/recetas/generar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mensaje })
        });

        if (!response.ok) throw new Error('Error del servidor');

        const data = await response.json();
        mostrarReceta(data);
    } catch (error) {
        rightPanel.innerHTML = `
            <div class="alert alert-danger m-4">
                <i class="bi bi-exclamation-triangle"></i> 
                Error al conectar con el servidor. Asegúrate de que Ollama y FastAPI están corriendo.
                <br><small class="text-muted">${error.message}</small>
            </div>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-magic"></i> Generar Receta';
    }
}

// Muestra la receta formateada en el panel derecho
function mostrarReceta(data) {
    const receta = data.receta;
    const preferencias = data.preferencias;
    const htmlReceta = convertirRecetaAHTML(receta, preferencias);
    document.getElementById('rightPanel').innerHTML = htmlReceta;
}

// Convierte el markdown de la receta a HTML con clases CSS para estilo
function convertirRecetaAHTML(markdown, prefs) {
    // Escapar HTML básico
    let html = markdown
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Encabezados<i class="bi bi-card-list">
    html = html.replace(/^##\s+(.*)$/gm, '<h2 class="recipe-title">$1</h2>');
    html = html.replace(/^###\s+(.*)$/gm, '<h3 class="section-title"></i> $1</h3>');

    // Negritas
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Listas de ingredientes (líneas que empiezan con -)
    html = html.replace(/^- (.*)$/gm, '<li>$1</li>');
    html = html.replace(/((?:<li>.*<\/li>\s*)+)/g, '<ul class="ingredient-list">$1</ul>');

    // Listas numeradas (pasos)
    html = html.replace(/^\d+\.\s+(.*)$/gm, '<li>$1</li>');
    html = html.replace(/((?:<li>.*<\/li>\s*)+)/g, function(match) {
        // Solo envolver si no está ya envuelto en <ul>
        if (!match.includes('<ul')) {
            return '<ol class="step-list">' + match + '</ol>';
        }
        return match;
    });

    // Listas numeradas
    html = html.replace(/^\d+\.\s+(.*)$/gm, '<li>$1</li>');
    html = html.replace(/((?:<li>.*<\/li>\s*)+)/g, function(match) {
        if (!match.includes('<ul') && !match.includes('<ol')) {
            return '<ol class="step-list">' + match + '</ol>';
        }
        return match;
    });

    // Envolver consejo del chef en un div especial (si aparece "Consejo del Chef")
    html = html.replace(
        /(<h3[^>]*>.*?Consejo.*?<\/h3>\s*)([\s\S]*?)(?=<h3|$)/i,
        function(match, header, content) {
            return header + '<div class="chef-tip">' + content.trim() + '</div>';
        }
    );

    // Envolver en tarjeta<i class="bi bi-download"></i><i class="bi bi-clock"></i><i class="bi bi-egg-fill"></i>
    return `
        <div class="recipe-card">
            ${html}
            <div class="d-flex justify-content-between mt-4">
                <button class="download-btn" onclick="descargarPDF()">
                     Descargar PDF
                </button>
                <span class="text-muted align-self-center">
                     ${prefs.tiempo} min • 
                     ${prefs.ingrediente}
                </span>
            </div>
        </div>
    `;
}

// Descarga la receta en PDF usando jsPDF
function descargarPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const card = document.querySelector('.recipe-card');
    if (!card) return;

// Extraer título
    const titleEl = card.querySelector('.recipe-title');
    const titulo = titleEl ? titleEl.textContent.trim() : 'Receta';
    
    // Limpiar título para nombre de archivo
    const nombreArchivo = titulo
        .replace(/[^a-záéíóúñü0-9\s-]/gi, '')
        .replace(/\s+/g, '-')
        .toLowerCase() + '.pdf';

    // Extraer metadatos (tiempo, ingrediente principal)
    const metaText = card.querySelector('.text-muted.align-self-center')?.textContent || '';
    
    // Extraer ingredientes (lista con clase ingredient-list)
    const ingredientesList = card.querySelector('.ingredient-list');
    const ingredientes = ingredientesList 
        ? Array.from(ingredientesList.querySelectorAll('li')).map(li => '• ' + li.textContent.trim())
        : [];
    
    // Extraer pasos (lista con clase step-list)
    const pasosList = card.querySelector('.step-list');
    const pasos = pasosList 
        ? Array.from(pasosList.querySelectorAll('li')).map((li, i) => `${i+1}. ${li.textContent.trim()}`)
        : [];
    
    // Extraer consejo (div con clase chef-tip)
    const consejoDiv = card.querySelector('.chef-tip');
    const consejo = consejoDiv ? consejoDiv.textContent.trim() : '';

    // Función para limpiar texto de caracteres extraños
    const limpiar = (str) => str
        .replace(/[^\x20-\x7EáéíóúñüÁÉÍÓÚÑÜ\u00f1\u00d1]/g, '') // solo ASCII extendido básico
        .replace(/\s+/g, ' ')
        .trim();

    // Construir PDF
    let y = 20;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text(limpiar(titulo), 20, y);
    y += 12;

    // Metadatos
    if (metaText) {
        doc.setFont("helvetica", "normal");
        doc.setFontSize(11);
        doc.text(limpiar(metaText), 20, y);
        y += 10;
    }

    // Ingredientes
    if (ingredientes.length > 0) {
        y += 5;
        doc.setFont("helvetica", "bold");
        doc.setFontSize(14);
        doc.text("Ingredientes", 20, y);
        y += 8;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(11);
        ingredientes.forEach(item => {
            const lines = doc.splitTextToSize(limpiar(item), 170);
            doc.text(lines, 20, y);
            y += lines.length * 5;
        });
    }

    // Preparación
    if (pasos.length > 0) {
        y += 5;
        doc.setFont("helvetica", "bold");
        doc.setFontSize(14);
        doc.text("Preparación", 20, y);
        y += 8;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(11);
        pasos.forEach(item => {
            const lines = doc.splitTextToSize(limpiar(item), 170);
            doc.text(lines, 20, y);
            y += lines.length * 5;
        });
    }

    // Consejo
    if (consejo) {
        y += 5;
        doc.setFont("helvetica", "bold");
        doc.setFontSize(14);
        doc.text("Consejo del Chef", 20, y);
        y += 8;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(11);
        const lines = doc.splitTextToSize(limpiar(consejo), 170);
        doc.text(lines, 20, y);
    }

    doc.save(nombreArchivo);
}

// -----------------------------
// LOGOUT
// -----------------------------
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}



// -----------------------------
// ALERTAS VISUALES
// -----------------------------
function showAlert(containerId, message, type="danger") {
    document.getElementById(containerId).innerHTML = `
        <div class="alert alert-${type}">${message}</div>
    `;
}
