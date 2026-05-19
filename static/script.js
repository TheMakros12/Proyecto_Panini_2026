let fullAlbumData = null;
let activeUser = localStorage.getItem('panini_user') || 'MarcosDB12';

const FLAGS_CODES = {
    "MEX": "mx", "RSA": "za", "KOR": "kr", "CZE": "cz",
    "CAN": "ca", "BIH": "ba", "QAT": "qa", "SUI": "ch",
    "BRA": "br", "MAR": "ma", "HAI": "ht", "SCO": "gb-sct",
    "USA": "us", "PAR": "py", "AUS": "au", "TUR": "tr",
    "GER": "de", "CUW": "cw", "CIV": "ci", "ECU": "ec",
    "NED": "nl", "JPN": "jp", "SWE": "se", "TUN": "tn",
    "BEL": "be", "EGY": "eg", "IRN": "ir", "NZL": "nz",
    "ESP": "es", "CPV": "cv", "KSA": "sa", "URU": "uy",
    "FRA": "fr", "SEN": "sn", "IRQ": "iq", "NOR": "no",
    "ARG": "ar", "ALG": "dz", "AUT": "at", "JOR": "jo",
    "POR": "pt", "COD": "cd", "UZB": "uz", "COL": "co",
    "ENG": "gb-eng", "CRO": "hr", "GHA": "gh", "PAN": "pa"
};

const TEAM_FULL_NAMES = {
    "FWC": "Copa Mundial FIFA",
    "FWC1": "Copa Mundial FIFA",
    "FWC2": "Copa Mundial FIFA",
    "MEX": "México",
    "RSA": "Sudáfrica",
    "KOR": "Corea del Sur",
    "CZE": "República Checa",
    "CAN": "Canadá",
    "BIH": "Bosnia y Herzegovina",
    "QAT": "Catar",
    "SUI": "Suiza",
    "BRA": "Brasil",
    "MAR": "Marruecos",
    "HAI": "Haití",
    "SCO": "Escocia",
    "USA": "Estados Unidos",
    "PAR": "Paraguay",
    "AUS": "Australia",
    "TUR": "Turquía",
    "GER": "Alemania",
    "CUW": "Curazao",
    "CIV": "Costa de Marfil",
    "ECU": "Ecuador",
    "NED": "Países Bajos",
    "JPN": "Japón",
    "SWE": "Suecia",
    "TUN": "Túnez",
    "BEL": "Bélgica",
    "EGY": "Egipto",
    "IRN": "Irán",
    "NZL": "Nueva Zelanda",
    "ESP": "España",
    "CPV": "Cabo Verde",
    "KSA": "Arabia Saudita",
    "URU": "Uruguay",
    "FRA": "Francia",
    "SEN": "Senegal",
    "IRQ": "Irak",
    "NOR": "Noruega",
    "ARG": "Argentina",
    "ALG": "Argelia",
    "AUT": "Austria",
    "JOR": "Jordania",
    "POR": "Portugal",
    "COD": "República Democrática del Congo",
    "UZB": "Uzbekistán",
    "COL": "Colombia",
    "ENG": "Inglaterra",
    "CRO": "Croacia",
    "GHA": "Ghana",
    "PAN": "Panamá",
    "CC": "Clásicos / Leyendas"
};


function getTeamName(equipo) {
    let eq = (equipo === 'FWC1' || equipo === 'FWC2') ? 'FWC' : equipo;
    if (eq === 'FWC') return '🏆 FWC';
    if (eq === 'CC') return '✨ CC';
    
    let code = FLAGS_CODES[eq];
    if (code) {
        return `<img src="https://flagcdn.com/24x18/${code}.png" alt="${eq} flag" class="team-flag"> ${eq}`;
    }
    return eq;
}

document.addEventListener('DOMContentLoaded', () => {
    // PWA Service Worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(err => console.log('SW ref', err));
    }

    loadUsers();
    loadAllData();
    switchTab('dashboard');

    document.getElementById('add-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('cromo-input');
        const ids = input.value;
        
        try {
            const res = await fetch('/api/tengo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ids, user_id: activeUser })
            });
            const data = await res.json();
            
            if (data.success) {
                input.value = '';
                showToast(`¡Guardados: ${data.registrados.join(', ')}!`);
                loadAllData();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

async function loadUsers() {
    const res = await fetch('/api/usuarios');
    let usuarios = await res.json();
    
    if (!usuarios.includes(activeUser)) {
        usuarios.push(activeUser);
    }
    
    const select = document.getElementById('user-select');
    select.innerHTML = '';
    usuarios.forEach(u => {
        const opt = document.createElement('option');
        opt.value = u;
        opt.innerText = u;
        if (u === activeUser) opt.selected = true;
        select.appendChild(opt);
    });
}

function changeUser() {
    activeUser = document.getElementById('user-select').value;
    localStorage.setItem('panini_user', activeUser);
    loadAllData();
}

function createNewUser() {
    const newName = prompt("Introduce el nombre del nuevo usuario (sin espacios raros):");
    if (newName && newName.trim()) {
        activeUser = newName.trim();
        localStorage.setItem('panini_user', activeUser);
        loadUsers();
        loadAllData();
    }
}

function loadAllData() {
    loadStats();
    loadAlbum();
    loadHistory();
    renderTeamsCompactCards();
}

async function loadHistory() {
    const res = await fetch(`/api/historial?user_id=${encodeURIComponent(activeUser)}`);
    const history = await res.json();
    
    const list = document.getElementById('history-list');
    list.innerHTML = '';
    
    if (history.length === 0) {
        list.innerHTML = '<li class="history-item" style="justify-content:center;color:var(--text-muted)">Sin actividad reciente</li>';
        return;
    }
    
    history.forEach(item => {
        const li = document.createElement('li');
        li.className = `history-item ${item.accion === 'añadido' ? 'added' : 'removed'}`;
        const time = new Date(item.fecha).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        li.innerHTML = `<span>${item.cromo_id} <small>(${item.accion})</small></span> <span class="hist-time">${time}</span>`;
        list.appendChild(li);
    });
}

function formatRanges(numeros) {
    if (!numeros || numeros.length === 0) return "";
    numeros.sort((a, b) => a - b);
    let rangos = [];
    let inicio = numeros[0];
    let fin = numeros[0];
    for (let i = 1; i < numeros.length; i++) {
        let n = numeros[i];
        if (n === fin + 1) {
            fin = n;
        } else {
            let startStr = inicio === 0 ? "00" : inicio.toString();
            let endStr = fin === 0 ? "00" : fin.toString();
            rangos.push(inicio === fin ? startStr : `${startStr}-${endStr}`);
            inicio = fin = n;
        }
    }
    let startStr = inicio === 0 ? "00" : inicio.toString();
    let endStr = fin === 0 ? "00" : fin.toString();
    rangos.push(inicio === fin ? startStr : `${startStr}-${endStr}`);
    return rangos.join(', ');
}

async function loadStats() {
    const res = await fetch(`/api/stats?user_id=${encodeURIComponent(activeUser)}`);
    const data = await res.json();
    
    document.getElementById('val-conseguidos').innerText = data.conseguidos;
    document.getElementById('val-faltantes').innerText = data.faltantes;
    document.getElementById('val-repetidos').innerText = data.repetidos;
    document.getElementById('val-porcentaje').innerText = `${data.porcentaje}%`;
    
    const circle = document.getElementById('progress-circle');
    circle.style.background = `conic-gradient(var(--accent) ${data.porcentaje}%, var(--glass-border) 0%)`;
}

async function loadAlbum() {
    const res = await fetch(`/api/album?user_id=${encodeURIComponent(activeUser)}`);
    fullAlbumData = await res.json();
    renderFaltantesFromAlbum();
    renderRepetidosFromAlbum();
    renderGroupProgress();
    renderTeamsCompactCards();
}

function renderFaltantesFromAlbum() {
    const container = document.getElementById('tab-faltantes');
    container.innerHTML = '';
    
    fullAlbumData.estructura.forEach(grupo => {
        const groupSection = document.createElement('div');
        groupSection.className = 'group-section';
        
        let hasContent = false;
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'grid-container group-grid';

        for (const equipo of grupo.equipos) {
            const cromos = fullAlbumData.cromos[equipo] || [];
            const faltantes = cromos.filter(c => c.cantidad === 0).map(c => c.numero);
            
            if (faltantes.length > 0) {
                hasContent = true;
                const card = document.createElement('div');
                const teamInfo = TEAM_COLORS[equipo] || { flag: '⚽' };
                const fullName = TEAM_FULL_NAMES[equipo] || equipo;
                const crestPath = `/assets/crests/${equipo.toLowerCase()}.png`;
                card.className = `team-card ${equipo.toLowerCase()}`;
                card.onclick = () => openModal(equipo);
                
                let total = cromos.length;
                let conseguidos = total - faltantes.length;
                let progress = total > 0 ? (conseguidos / total) * 100 : 0;
                
                card.innerHTML = `
                    <div class="team-header">
                        <span class="team-name">
                            <img src="${crestPath}" alt="${equipo}" class="team-flag-crest"
                                onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';">
                            <span class="team-flag-fallback" style="display:none;">${teamInfo.flag}</span>
                            ${fullName}
                        </span>
                        <span class="team-count">Faltan ${faltantes.length}</span>
                    </div>
                    <div class="team-numbers">${formatRanges(faltantes)}</div>
                    <div class="progress-bg">
                        <div class="progress-bar" style="width: ${progress}%"></div>
                    </div>
                `;
                cardsContainer.appendChild(card);
            }
        }
        
        if (hasContent) {
            const title = document.createElement('h3');
            title.className = 'group-title';
            title.innerText = grupo.nombre;
            groupSection.appendChild(title);
            groupSection.appendChild(cardsContainer);
            container.appendChild(groupSection);
        }
    });
}

function renderRepetidosFromAlbum() {
    const container = document.getElementById('tab-repetidos');
    container.innerHTML = '';
    
    let hayRepetidos = false;
    
    fullAlbumData.estructura.forEach(grupo => {
        const groupSection = document.createElement('div');
        groupSection.className = 'group-section';
        let groupHasContent = false;
        
        const cardsContainer = document.createElement('div');
        cardsContainer.className = 'grid-container group-grid';

        for (const equipo of grupo.equipos) {
            const cromos = fullAlbumData.cromos[equipo] || [];
            const repetidos = cromos.filter(c => c.cantidad > 1);
            
            if (repetidos.length > 0) {
                hayRepetidos = true;
                groupHasContent = true;
                const textArr = repetidos.map(i => {
                    let numStr = i.numero === 0 ? "00" : i.numero;
                    return i.cantidad > 2 ? `${numStr}(x${i.cantidad-1})` : numStr;
                });
                
                const teamInfo = TEAM_COLORS[equipo] || { flag: '⚽' };
                const fullName = TEAM_FULL_NAMES[equipo] || equipo;
                const crestPath = `/assets/crests/${equipo.toLowerCase()}.png`;
                
                let total = cromos.length;
                let faltantes = cromos.filter(c => c.cantidad === 0).length;
                let conseguidos = total - faltantes;
                let progress = total > 0 ? (conseguidos / total) * 100 : 0;
                
                const card = document.createElement('div');
                card.className = `team-card ${equipo.toLowerCase()}`;
                card.onclick = () => openModal(equipo);
                card.innerHTML = `
                    <div class="team-header">
                        <span class="team-name">
                            <img src="${crestPath}" alt="${equipo}" class="team-flag-crest"
                                onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';">
                            <span class="team-flag-fallback" style="display:none;">${teamInfo.flag}</span>
                            ${fullName}
                        </span>
                        <span class="team-count">${repetidos.length} repetidos</span>
                    </div>
                    <div class="team-numbers">${textArr.join(', ')}</div>
                    <div class="progress-bg">
                        <div class="progress-bar" style="width: ${progress}%"></div>
                    </div>
                `;
                cardsContainer.appendChild(card);
            }
        }
        
        if (groupHasContent) {
            const title = document.createElement('h3');
            title.className = 'group-title';
            title.innerText = grupo.nombre;
            groupSection.appendChild(title);
            groupSection.appendChild(cardsContainer);
            container.appendChild(groupSection);
        }
    });
    
    if (!hayRepetidos) {
        container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); font-size: 1.2rem;">No tienes cromos repetidos aún.</div>';
    }
}

function openModal(equipo) {
    const title = document.getElementById('modal-title');
    const grid = document.getElementById('modal-grid');
    
    // Ruta del escudo (en minúsculas para compatibilidad en Linux/Railway)
    const crestPath = `/assets/crests/${equipo.toLowerCase()}.png`;
    const teamInfo = TEAM_COLORS[equipo] || { flag: '⚽' };
    const fullName = TEAM_FULL_NAMES[equipo] || equipo;

    title.innerHTML = `
        <div class="modal-title-container">
            <img 
                src="${crestPath}" 
                alt="${equipo}" 
                class="modal-team-crest"
                onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
            >
            <div class="modal-team-crest-fallback" style="display: none;">
                ${teamInfo.flag}
            </div>
            <span class="modal-team-name">${fullName}</span>
        </div>
    `;
    grid.innerHTML = '';
    
    const toggle = document.getElementById('mode-toggle');
    const modalContent = document.querySelector('.modal-content');
    const labelAdd = document.getElementById('label-add');
    const labelRemove = document.getElementById('label-remove');
    
    toggle.checked = false;
    modalContent.classList.remove('delete-mode');
    labelAdd.classList.add('active-add');
    labelRemove.classList.remove('active-remove');
    
    toggle.onchange = (e) => {
        if (e.target.checked) {
            modalContent.classList.add('delete-mode');
            labelAdd.classList.remove('active-add');
            labelRemove.classList.add('active-remove');
        } else {
            modalContent.classList.remove('delete-mode');
            labelAdd.classList.add('active-add');
            labelRemove.classList.remove('active-remove');
        }
    };
    
    const cromos = fullAlbumData.cromos[equipo] || [];
    
    cromos.forEach(c => {
        const btnContainer = document.createElement('div');
        btnContainer.className = 'cromo-item';
        
        const btn = document.createElement('button');
        btn.className = 'cromo-btn';
        let numStr = c.numero === 0 ? '00' : c.numero;
        btn.innerText = numStr;
        
        const nameLabel = document.createElement('div');
        nameLabel.className = 'cromo-name';
        nameLabel.innerText = c.nombre || '-';
        nameLabel.onclick = (e) => {
            e.stopPropagation();
            const newName = prompt(`Nombre para ${equipo} ${numStr}:`, c.nombre || '');
            if (newName !== null) {
                updatePlayerName(equipo, c.numero, newName);
            }
        };
        
        if (c.cantidad === 1) btn.classList.add('got');
        if (c.cantidad > 1) {
            btn.classList.add('rep');
            btn.innerText = `${numStr} (+${c.cantidad-1})`;
        }
        
        btn.onclick = async () => {
            const isDelete = document.getElementById('mode-toggle').checked;
            
            if (isDelete && c.cantidad === 0) return;
            
            btn.style.opacity = '0.5';
            const dbEquipo = equipo.startsWith('FWC') ? 'FWC' : equipo;
            
            if (isDelete) {
                await fetch('/api/quitar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ids: `${dbEquipo} ${c.numero}`, user_id: activeUser })
                });
                c.cantidad -= 1;
                showToast(`¡Borrado: ${dbEquipo} ${c.numero}!`);
            } else {
                await fetch('/api/tengo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ids: `${dbEquipo} ${c.numero}`, user_id: activeUser })
                });
                c.cantidad += 1;
                showToast(`¡Añadido: ${dbEquipo} ${c.numero}!`);
            }
            
            btn.style.opacity = '1';
            btn.className = 'cromo-btn'; 
            let numStr = c.numero === 0 ? '00' : c.numero;
            btn.innerText = numStr;
            
            if (c.cantidad === 1) btn.classList.add('got');
            if (c.cantidad > 1) {
                btn.classList.add('rep');
                btn.innerText = `${numStr} (+${c.cantidad-1})`;
            }
            
            loadAllData();
        };
        
        btnContainer.appendChild(btn);
        btnContainer.appendChild(nameLabel);
        grid.appendChild(btnContainer);
    });
    
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
}

function switchTab(tabId) {
    // Top Tabs (PC)
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.innerText.toLowerCase().includes(tabId)) btn.classList.add('active');
    });

    // Bottom Nav (Mobile/Web)
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        const labelEl = item.querySelector('.nav-label');
        if (labelEl) {
            const label = labelEl.innerText.toLowerCase();
            if (label === 'stats' && tabId === 'dashboard') item.classList.add('active');
            if (label === 'álbum' && tabId === 'faltantes') item.classList.add('active');
            if (label === 'repes' && tabId === 'repetidos') item.classList.add('active');
        }
    });

    // Content visibility
    const dashboardSections = [
        document.querySelector('.main-layout'),
        document.getElementById('group-progress-section'),
        document.getElementById('teams-compact-section'),
        document.querySelector('.action-buttons')
    ];

    if (tabId === 'dashboard') {
        dashboardSections.forEach(s => s?.classList.remove('hidden'));
        document.getElementById('tab-faltantes').classList.add('hidden');
        document.getElementById('tab-repetidos').classList.add('hidden');
    } else {
        dashboardSections.forEach(s => s?.classList.add('hidden'));
        document.getElementById('tab-faltantes').classList.add('hidden');
        document.getElementById('tab-repetidos').classList.add('hidden');
        
        const targetTab = document.getElementById(`tab-${tabId}`);
        if (targetTab) targetTab.classList.remove('hidden');
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderGroupProgress() {
    const grid = document.getElementById('group-progress-grid');
    if (!grid) return;
    grid.innerHTML = '';

    fullAlbumData.estructura.forEach(grupo => {
        let total = 0;
        let conseguidos = 0;

        grupo.equipos.forEach(equipo => {
            const cromos = fullAlbumData.cromos[equipo] || [];
            total += cromos.length;
            conseguidos += cromos.filter(c => c.cantidad > 0).length;
        });

        const progress = total > 0 ? Math.round((conseguidos / total) * 100) : 0;

        const card = document.createElement('div');
        card.className = 'group-mini-card';
        card.onclick = () => {
            switchTab('faltantes');
            setTimeout(() => {
                const groupTitle = Array.from(document.querySelectorAll('.group-title')).find(el => el.innerText === grupo.nombre);
                if (groupTitle) groupTitle.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        };

        card.innerHTML = `
            <div class="group-mini-header">
                <span>${grupo.nombre}</span>
                <span>${progress}%</span>
            </div>
            <div class="group-mini-bar-bg">
                <div class="group-mini-bar-fill" style="width: ${progress}%"></div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.innerText = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// Fallback for HTTP local network copying
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        const successful = document.execCommand('copy');
        if (successful) showToast("¡Copiado al portapapeles!");
        else showToast("No se pudo copiar automáticamente.");
    } catch (err) {
        console.error('Fallback: Error al copiar', err);
        showToast("Error al copiar.");
    }
    document.body.removeChild(textArea);
}

function copyTextToClipboard(text) {
    if (!navigator.clipboard || !window.isSecureContext) {
        fallbackCopyTextToClipboard(text);
        return;
    }
    navigator.clipboard.writeText(text).then(function() {
        showToast("¡Copiado al portapapeles!");
    }).catch(function(err) {
        console.error('Async: Error al copiar', err);
        fallbackCopyTextToClipboard(text);
    });
}

// WhatsApp Copy Functions
async function copyFaltantes() {
    const res = await fetch(`/api/faltantes?user_id=${encodeURIComponent(activeUser)}`);
    const faltantes = await res.json();
    
    let text = "📖 *Me faltan del Mundial 2026:*\n\n";
    let keys = Object.keys(faltantes);
    if(keys.length === 0) {
        text = "¡He completado el álbum! 🎉";
    } else {
        keys.forEach(eq => {
            text += `*${eq}*: ${formatRanges(faltantes[eq])}\n`;
        });
    }
    
    copyTextToClipboard(text);
}

async function copyRepetidos() {
    const res = await fetch(`/api/repetidos?user_id=${encodeURIComponent(activeUser)}`);
    const repetidos = await res.json();
    
    let text = "🔄 *Mis repetidos del Mundial 2026:*\n\n";
    let keys = Object.keys(repetidos);
    if(keys.length === 0) {
        text = "No tengo repetidos todavía.";
    } else {
        keys.forEach(eq => {
            let nums = repetidos[eq].map(c => {
                let numStr = c.numero === 0 ? "00" : c.numero;
                return c.cantidad > 2 ? `${numStr}(x${c.cantidad-1})` : numStr;
            });
            text += `*${eq}*: ${nums.join(', ')}\n`;
        });
    }
    
    copyTextToClipboard(text);
}

async function updatePlayerName(equipo, numero, nombre) {
    const dbEquipo = equipo.startsWith('FWC') ? 'FWC' : equipo;
    const res = await fetch('/api/update_name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: `${dbEquipo} ${numero}`, nombre, user_id: activeUser })
    });
    const data = await res.json();
    if (data.success) {
        showToast("Nombre actualizado");
        loadAllData();
        // Opcional: refrescar modal si sigue abierto
        const modalVisible = !document.getElementById('modal-overlay').classList.contains('hidden');
        if (modalVisible) {
            setTimeout(() => openModal(equipo), 100);
        }
    }
}

/* ========================================
   OPCIÓN 2: TARJETAS COMPACTAS CON ESCUDOS
   ======================================== */

// Mapeo de códigos de equipo a colores
const TEAM_COLORS = {
    'ARG': { class: 'arg', flag: '🇦🇷' },
    'ESP': { class: 'esp', flag: '🇪🇸' },
    'FRA': { class: 'fra', flag: '🇫🇷' },
    'BRA': { class: 'bra', flag: '🇧🇷' },
    'ALE': { class: 'ale', flag: '🇩🇪' },
    'POR': { class: 'por', flag: '🇵🇹' },
    'ITA': { class: 'ita', flag: '🇮🇹' },
    'URU': { class: 'uru', flag: '🇺🇾' },
    'MEX': { class: 'mex', flag: '🇲🇽' },
    'ENG': { class: 'eng', flag: '🇬🇧' },
    'CAN': { class: 'can', flag: '🇨🇦' },
    'USA': { class: 'usa', flag: '🇺🇸' },
    'COL': { class: 'col', flag: '🇨🇴' },
    'PAR': { class: 'par', flag: '🇵🇾' },
    'NED': { class: 'ned', flag: '🇳🇱' },
    'BEL': { class: 'bel', flag: '🇧🇪' },
    'JPN': { class: 'jpn', flag: '🇯🇵' },
    'SUI': { class: 'sui', flag: '🇨🇭' },
    'SWE': { class: 'swe', flag: '🇸🇪' },
    'NOR': { class: 'nor', flag: '🇳🇴' },
    'CRO': { class: 'cro', flag: '🇭🇷' },
    'GER': { class: 'ger', flag: '🇩🇪' },
    'SEN': { class: 'sen', flag: '🇸🇳' },
    'MAR': { class: 'mar', flag: '🇲🇦' },
    'HAI': { class: 'hai', flag: '🇭🇹' },
    'GHA': { class: 'gha', flag: '🇬🇭' },
    'EGY': { class: 'egy', flag: '🇪🇬' },
    'FWC': { class: 'fwc', flag: '🏆' },
    'CC': { class: 'cc', flag: '✨' },
};

function openGroupModal(equipo) {
    openModal(equipo);
}

function renderTeamsCompactCards() {
    if (!fullAlbumData) return;

    const container = document.getElementById('teams-compact-grid');
    if (!container) return;

    container.innerHTML = '';

    const { estructura, cromos } = fullAlbumData;

    // Crear lista ordenada de equipos
    const teamsToRender = [];
    estructura.forEach(group => {
        group.equipos.forEach(equipo => {
            if (cromos[equipo] && cromos[equipo].length > 0) {
                teamsToRender.push(equipo);
            }
        });
    });

    // Renderizar cada tarjeta
    teamsToRender.forEach(equipo => {
        const cromosEquipo = cromos[equipo] || [];
        const conseguidos = cromosEquipo.filter(c => c.cantidad >= 1).length;
        const total = cromosEquipo.length;
        const porcentaje = total > 0 ? Math.round((conseguidos / total) * 100) : 0;

        const card = createTeamCompactCard(equipo, conseguidos, total, porcentaje);
        container.appendChild(card);
    });
}

function createTeamCompactCard(equipo, conseguidos, total, porcentaje) {
    const card = document.createElement('div');
    const teamInfo = TEAM_COLORS[equipo] || { flag: '⚽' };
    const isCompleted = conseguidos === total && total > 0;

    // Clases dinámicas - siempre usar el código del equipo en minúsculas para el CSS de color
    const classes = ['team-compact-card', equipo.toLowerCase()];
    if (isCompleted) classes.push('completed');
    if (conseguidos === 0) classes.push('empty');

    card.className = classes.join(' ');
    card.onclick = () => openGroupModal(equipo); // Abre el modal del equipo

    // Ruta del escudo (en minúsculas para compatibilidad en Linux/Railway)
    const crestPath = `/assets/crests/${equipo.toLowerCase()}.png`;

    card.innerHTML = `
        <div class="team-compact-header">
            <img 
                src="${crestPath}" 
                alt="${equipo}" 
                class="team-crest"
                onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
            >
            <div class="team-crest-fallback" style="display: none;">
                ${teamInfo.flag}
            </div>
            <div class="team-compact-info">
                <p class="team-compact-name">${equipo}</p>
                <p class="team-compact-count">${conseguidos}/${total}</p>
            </div>
        </div>
        <div class="team-compact-progress">
            <div class="team-compact-progress-fill" style="width: ${porcentaje}%;"></div>
        </div>
    `;

    return card;
}
