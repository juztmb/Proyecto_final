// Configuración de las rutas de la API del backend (ajusta a tu entorno real)
const API_BASE = 'http://localhost:8000/cliente';

const CREST_COLORS = ['#38bdf8', '#10b981', '#ef4444', '#eab308', '#3b82f6', '#a855f7'];
let selectedCrestColor = CREST_COLORS[0];
let teams = [
   
  ];
async function verificarYFetch() {
   
    const miVariable = localStorage.getItem('userinfo');
    
    
    if (miVariable) {
        console.log('Variable encontrada. Solicitando datos a la API local...');
        console.log(miVariable)
        try {
            const iniciales = document.querySelector('.avatar-persona')
            const nombreUser = document.querySelector('.nombre-persona')
            const texto_iniciales = JSON.parse(miVariable).nombre_usuario
            console.log(texto_iniciales)
            if (texto_iniciales != null){
              iniciales.innerText = texto_iniciales.slice(0,2)
              nombreUser.innerText = texto_iniciales
            }
          
            const usuario_id = JSON.parse(miVariable).id
            const respuesta = await fetch(`${API_BASE}/equiposByIdUsuario/${usuario_id}`);
            const respuestaJson = await respuesta.json()
            console.log(respuesta)
            if (!respuesta.ok) {
                throw new Error(`Error en la petición: ${respuesta.status}`);
            }

            console.log(respuestaJson)
            
            
            console.log('Datos cargados con éxito:', respuestaJson);
            procesarDatosAPI(respuestaJson); 

        } catch (error) {
            console.error('Hubo un problema con la API local:', error);
        }
    } else {
        console.log('Sesion no iniciada');
        alert('Por favor inicie sesion')
        window.location.href = "../index.html";
    }
}


document.addEventListener('DOMContentLoaded', verificarYFetch);


function procesarDatosAPI(datos) {
    console.log(datos)
    datos.forEach((equipo) => teams.push(equipo));
    renderTeams()


}





let selectedTeamId = teams.length ? teams[0].id : null;

function posLabel(pos){
    return { delantero:'Delantero', medio:'Medio', defensa:'Defensa', portero:'Portero' }[pos] || pos;
  }

function renderCrestPicker(){
    const wrap = document.getElementById('crestPicker');
    wrap.innerHTML = '';
    CREST_COLORS.forEach(c => {
      const el = document.createElement('div');
      el.className = 'crest-opt' + (c === selectedCrestColor ? ' selected' : '');
      el.style.background = c;
      el.onclick = () => { selectedCrestColor = c; renderCrestPicker(); };
      wrap.appendChild(el);
    });
  }

function renderStats(){
    const totalPlayers = teams.reduce((sum, t) => sum + t.players.length, 0);
    const totalPoints = teams.reduce((sum, t) => sum + t.points, 0);
    document.getElementById('statTeams').textContent = teams.length;
    document.getElementById('statPlayers').textContent = totalPlayers;
    document.getElementById('statPoints').textContent = totalPoints;
  }

function renderTeams(){
    const grid = document.getElementById('teamsGrid');
    grid.innerHTML = '';
    document.getElementById('teamsCount').textContent = teams.length + (teams.length === 1 ? ' equipo' : ' equipos');

    teams.forEach(team => {
      const card = document.createElement('div');
      card.className = 'team-card' + (team.id === selectedTeamId ? ' selected' : '');
      card.onclick = () => selectTeam(team.id);
      card.innerHTML = `
        <button class="del-btn" title="Eliminar equipo" onclick="event.stopPropagation(); deleteTeam('${team.id}')">🗑</button>
        <div class="crest" style="background:${team.crest}">${team.name.slice(0,2).toUpperCase()}</div>
        <h3>${team.name}</h3>
        <div class="sub">${team.players.length} jugador${team.players.length === 1 ? '' : 'es'}</div>
        <div class="row"><span>Puntos totales</span><span class="pts">${team.points}</span></div>
      `;
      grid.appendChild(card);
    });

const addCard = document.createElement('div');
    addCard.className = 'team-card add-new';
    addCard.onclick = () => openModal('teamOverlay');
    addCard.innerHTML = `<div class="plus">+</div><div>Crear nuevo equipo</div>`;
    grid.appendChild(addCard);

    renderStats();
  }

function selectTeam(id){
    selectedTeamId = id;
    renderTeams();
    renderRoster();
  }

function renderRoster(){
    const panel = document.getElementById('rosterPanel');
    const team = teams.find(t => t.id === selectedTeamId);

    if(!team){
      document.getElementById('rosterTitle').textContent = 'Plantilla';
      panel.innerHTML = '<div class="roster-empty">Selecciona un equipo arriba para ver y editar su plantilla.</div>';
      return;
    }

    document.getElementById('rosterTitle').textContent = 'Plantilla — ' + team.name;

    panel.innerHTML = `
      <div class="roster-head">
        <h2><span class="mini-crest" style="background:${team.crest}">${team.name.slice(0,2).toUpperCase()}</span>${team.name}</h2>
        <button class="btn-outline" onclick="openModal('playerOverlay')">+ Agregar jugador</button>
      </div>
      <div class="roster-body">
        <div class="player-list" id="playerListWrap"></div>
        <div class="add-player-box">
          <h3>Resumen del equipo</h3>
          <p style="color:var(--muted); font-size:0.85rem; line-height:1.6; margin:0 0 14px;">
            ${team.players.length} jugadores registrados · ${team.points} puntos acumulados en el torneo.
          </p>
          <button class="btn-primary" style="width:100%;" onclick="openModal('playerOverlay')">+ Agregar jugador a este equipo</button>
        </div>
      </div>
    `;

    const listWrap = document.getElementById('playerListWrap');
    if(team.players.length === 0){
      listWrap.innerHTML = '<div class="roster-empty">Aún no hay jugadores en este equipo.</div>';
      return;
    }

    team.players.forEach(p => {
      const item = document.createElement('div');
      item.className = 'player-item';
      item.innerHTML = `
        <div class="p-left">
          <span class="badge ${p.posicion}">${posLabel(p.posicion)}</span>
          <span class="p-name">${p.nombre}</span>
        </div>
        <div class="p-stats">
          <span class="stat-chip">P: ${p.puntos}</span>
          <button class="p-remove" title="Quitar jugador" onclick="removePlayer('${team.id}','${p.id}')">✕</button>
        </div>
      `;
      listWrap.appendChild(item);
    });
  }

async function createTeam(e){
    e.preventDefault();
    const nameInput = document.getElementById('newTeamName');
    const name = nameInput.value.trim();
    const id_usuario = JSON.parse(localStorage.getItem('userinfo')).id
    console.log(name)
    
    if(!name) return false;

    const newTeam = {
        id_usuario: id_usuario,
      nombre_equipo : name,
      color: selectedCrestColor,
      
    };
    teams.push(newTeam);
    selectedTeamId = newTeam.id;

    const response = await fetch(`${API_BASE}/crear_equipo`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(newTeam) });
    const responseJson = await response.json()
    console.log(responseJson)
    nameInput.value = '';
    closeModal('teamOverlay');
    await actualizarEquipo();
    renderTeams();
    renderRoster();
    showToast(`Equipo "${name}" creado correctamente`);
    return false;
  }

async function deleteTeam(id){
    const team = teams.find(t => t.id === id);
    if(!team) return;
    if(!confirm(`¿Eliminar el equipo "${team.name}"? Esta acción no se puede deshacer.`)) return;
    const infoEliminar = {
        'usuario_id': JSON.parse(localStorage.getItem('userinfo')).id,
        'equipo_id' : id
    }
    const response = await fetch(`${API_BASE}/deleteEquipo`,
        {
            method: "DELETE",
            headers:{'Content-Type':'application/json'}, 
            body: JSON.stringify(infoEliminar) 
        }
    )
    const responseJson = await response.json()
    teams = teams.filter(t => t.id !== id);
    if(selectedTeamId === id){
      selectedTeamId = teams.length ? teams[0].id : null;
    }
    renderTeams();
    renderRoster();
    showToast('Equipo eliminado');
  }

function addPlayer(e){
    e.preventDefault();
    const team = teams.find(t => t.id === selectedTeamId);
    if(!team){
      showToast('Selecciona un equipo primero');
      closeModal('playerOverlay');
      return false;
    }

    if(!nombre) return false;

    const puntos = goles * 4 + asistencias * 3;
    const newPlayer = { id: 'p' + Date.now(), nombre, posicion, goles, asistencias, puntos };

    team.players.push(newPlayer);
    team.points += puntos;

  
    closeModal('playerOverlay');
    renderTeams();
    renderRoster();
    showToast(`${nombre} se unió a ${team.name}`);
    return false;
  }

async function removePlayer(teamId, playerId){
    const team = teams.find(t => t.id === teamId);
    if(!team) return;
    const player = team.players.find(p => p.id === playerId);
    if(!player) return;
    const infoEliminar={
      'jugador_id': playerId,
      'equipo_id': teamId
    }
    team.players = team.players.filter(p => p.id !== playerId);
    const response = await fetch(`${API_BASE}/deleteJugadorEquipo`,
        {
            method: "DELETE",
            headers:{'Content-Type':'application/json'}, 
            body: JSON.stringify(infoEliminar) 
        }
    )
    const responseJson = await response.json()
    console.log(responseJson)
    renderTeams();
    renderRoster();
    showToast(`${player.nombre} fue removido del equipo`);
  }

function openModal(id){
    if(id === 'teamOverlay') 
    {
      document.getElementById(id).classList.add('open')
      renderCrestPicker();
      const modal = document.getElementById(id).firstElementChild
      console.log(modal)
      modal.querySelector('.form-modal').classList.add('active')}
    if(id === 'playerOverlay'){
      document.getElementById(id).classList.add('open')
      const team = teams.find(t => t.id === selectedTeamId);
      document.getElementById('catalogTarget').textContent = team ? `Agregando a: ${team.name}` : 'Selecciona un equipo primero';
  }}

function closeModal(id){
    document.getElementById(id).classList.remove('open');
  }
  document.querySelectorAll('.overlay').forEach(ov => {
    ov.addEventListener('click', (e) => { if(e.target === ov) ov.classList.remove('open'); });
  });

  document.getElementById('btnNewTeamTop').addEventListener('click', () => openModal('teamOverlay'));

  document.getElementById('menuBtn').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
  });

  document.getElementById('searchInput').addEventListener('input', (e) => {
    const q = e.target.value.trim().toLowerCase();
    document.querySelectorAll('.team-card:not(.add-new)').forEach(card => {
      const name = card.querySelector('h3').textContent.toLowerCase();
      card.style.display = name.includes(q) ? '' : 'none';
    });
  });

let toastTimer;
function showToast(msg){
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2400);
  }

renderCrestPicker();


async function actualizarEquipo() {
    try {
            
            const miVariable = localStorage.getItem('userinfo')
            const usuario_id = JSON.parse(miVariable).id
            const respuesta = await fetch(`${API_BASE}/equiposByIdUsuario/${usuario_id}`);
            const respuestaJson = await respuesta.json()
            console.log(respuesta)
            if (!respuesta.ok) {
                throw new Error(`Error en la petición: ${respuesta.status}`);
            }

            console.log(respuestaJson)
            
            // 4. Hacer algo con la información recibida antes de que el usuario interactúe
            console.log('Datos cargados con éxito:', respuestaJson);
            teams = []
            procesarDatosAPI(respuestaJson); 

        } catch (error) {
            console.error('Hubo un problema con la API local:', error);
        }
}

let debounceTimer;

function filterCatalog() {
  const query = document.getElementById('catalogSearch').value.trim();
  const grid = document.getElementById('catalogGrid');

  
  clearTimeout(debounceTimer);

  
  if (query === '') {
    grid.innerHTML = '<div class="catalog-state">Escribe el nombre de un jugador para buscar...</div>';
    return;
  }

  
  grid.innerHTML = '<div class="catalog-state"><div class="spinner"></div>Buscando...</div>';

  
  debounceTimer = setTimeout(() => {
    fetchPlayersFromServer(query);
  }, 500); 
}


async function fetchPlayersFromServer(query) {
  const grid = document.getElementById('catalogGrid');

  try {
    
    const response = await fetch(`${API_BASE}/obtenerJugador/${query}`);
    
    if (!response.ok) {
      throw new Error('Error en la respuesta del servidor');
    }

    const players = await response.json();
    renderPlayerCards(players);

  } catch (error) {
    console.error('Error al obtener jugadores:', error);
    grid.innerHTML = '<div class="catalog-state">⚠️ Error al cargar los jugadores. Inténtalo de nuevo.</div>';
  }
}


function renderPlayerCards(players) {
  const grid = document.getElementById('catalogGrid');
  grid.innerHTML = '';

  if (players.length === 0) {
    grid.innerHTML = '<div class="catalog-state">No se encontraron jugadores.</div>';
    return;
  }

  
  players.forEach(player => {
    const card = document.createElement('div');
    card.className = 'player-card';
    
    card.innerHTML = `
      <div class="player-info ${player.id}">
        <h4>${player.nombre}</h4>
        <p class="player-position-badge player-position-${player.posicion}">${player.posicion || 'Sin posición'}</p>
        <p class="player-price">${player.precio} </p>
        <p>${player.equipo} </p>
      </div>
      <button class="btn-select" onclick="selectPlayer('${player.id}', '${player.name}')">Seleccionar</button>
    `;
    
    grid.appendChild(card);
  });
}


async function selectPlayer(id, name) {
  console.log(selectedTeamId);

  try{
  const response = await fetch(`${API_BASE}/agregar_jugador`, 
      { method:'POST', 
        headers:{'Content-Type':'application/json'}, 
        body: JSON.stringify({'jugador_id': id, 'equipo_id': selectedTeamId}) 
      });
    const responseJson = await response.json()
    console.log(responseJson)
    if (!response.ok) {
      console.log(responseJson.detail)
        switch (responseJson.detail.code) {
            case "FONDOS_INSUFICIENTES":
                console.log('fondos')
                alert('No cuentas con el dinero suficiente para este jugador')
                break;
        }
    }
    else{
      await actualizarEquipo();
      renderTeams();
      renderRoster();
      closeModal('playerOverlay');
    }
  
    
  }
  catch(error){
    console.log('error')
    alert('ocurrio un error al agregar el jugador')
  }
  
}