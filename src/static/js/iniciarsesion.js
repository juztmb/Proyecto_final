const API_BASE = 'http://localhost:8000/cliente'
function switchTab(which){
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabLogin = document.getElementById('tabLogin');
    const tabRegister = document.getElementById('tabRegister');

    if(which === 'login'){
      loginForm.classList.add('active');
      registerForm.classList.remove('active');
      tabLogin.classList.add('active');
      tabRegister.classList.remove('active');
    } else {
      registerForm.classList.add('active');
      loginForm.classList.remove('active');
      tabRegister.classList.add('active');
      tabLogin.classList.remove('active');
    }
  }

function togglePw(id, btn){
    const input = document.getElementById(id);
    const isPw = input.type === 'password';
    input.type = isPw ? 'text' : 'password';
    btn.textContent = isPw ? 'Ocultar' : 'Ver';
}

function checkStrength(value){
    const bar = document.getElementById('strengthBar');
    let score = 0;
    if(value.length >= 8) score++;
    if(/[A-Z]/.test(value)) score++;
    if(/[0-9]/.test(value)) score++;
    if(/[^A-Za-z0-9]/.test(value)) score++;

    const pct = (score / 4) * 100;
    bar.style.width = pct + '%';
    bar.style.background = score <= 1 ? '#ef4444' : score <= 2 ? '#eab308' : score <= 3 ? '#3b82f6' : '#10b981';
}

async function handleLogin(e){
    e.preventDefault();
    // Placeholder: conectar con el backend de autenticación real.
    //alert('Conecta este formulario a tu API de autenticación para iniciar sesión.');
    const email = document.getElementById('loginEmail').value
    const contrasena = document.getElementById('loginPassword').value
    body = {
      'correo': email,
      'contrasena': contrasena
    }
    console.log(body)
    try { 
      const response = await fetch(`${API_BASE}/login`, { 
        method: 'POST',                
        headers: { 'Content-Type': 'application/json' },                
        body: JSON.stringify(body)}); 
        const info = await response.json()
        console.log(info)         
        if (info.correo != null) {
          
          
          localStorage.setItem("userinfo", JSON.stringify(info));
          window.location.href = "../pages/dashboard.html";


        }

          
        else {
            console.log(info.id)                
            alert('Error en el servidor al intentar iniciar sesion.');}} 
    catch (error) {alert('No se pudo conectar con la API');}
    return false;
}

async function handleRegister(e){
    e.preventDefault();
    const pw = document.getElementById('regPassword').value;
    const confirm = document.getElementById('regPasswordConfirm').value;
    const confirmError = document.getElementById('regConfirmError');
    const confirmInput = document.getElementById('regPasswordConfirm');

    if(pw !== confirm){
      confirmError.classList.add('show');
      confirmInput.classList.add('invalid');
      return false;
    }
    confirmError.classList.remove('show');
    confirmInput.classList.remove('invalid');

    // Placeholder: conectar con el backend de registro real.
    const body = {
      'nombre': document.getElementById('nombreCom').value,
      'nombre_usuario': document.getElementById('userName').value,
      'correo': document.getElementById('regEmail').value,
      'contrasena': pw,
      'token': 'NA'
    }
    try { 
      const response = await fetch(`${API_BASE}/verificarE/${document.getElementById('regEmail').value}`, { 
        method: 'GET',                
        headers: { 'Content-Type': 'application/json' }}); 
        const info = await response.json()
        console.log(info)         
        if (info.existe) {
          
          alert('Este correo parece haber sido utilizado previamente intente iniciar sesion ');} 
        else {                
            alert('continuar');
            const reponseSubir = await fetch(`${API_BASE}/create`, { 
            method: 'POST',                
            headers: { 'Content-Type': 'application/json' },                
            body: JSON.stringify(body)});
            const info2 = await reponseSubir.json()
            if (info2.id != null){
              alert('se creo correctamente el usuario, por favor inicie sesion')
              console.log(info2.id)
            } 
              }} 
    catch (error) {alert('No se pudo conectar con la API');}
    return false;
}