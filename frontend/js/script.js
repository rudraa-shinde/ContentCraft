const API = 'http://127.0.0.1:5000';

// ── AUTH HELPERS ──
function getToken(){ return localStorage.getItem('token'); }
function getName(){  return localStorage.getItem('name');  }

function getUserId(){
  try{
    const p = JSON.parse(atob(getToken().split('.')[1]));
    return p.user_id;
  }catch{ return null; }
}

function authGuard(){
  if(!getToken()) window.location.href = 'login.html';
}

function logout(){
  localStorage.clear();
  window.location.href = 'login.html';
}

// ── SIDEBAR INIT ──
function initSidebar(){
  const name = getName() || 'User';
  const el1  = document.getElementById('sidebarName');
  const el2  = document.getElementById('avatarLetter');
  if(el1) el1.textContent = name;
  if(el2) el2.textContent = name[0].toUpperCase();
}

// ── ALERTS ──
function showAlert(type, msg, containerId=''){
  const id  = containerId || (type==='error' ? 'errorMsg' : 'successMsg');
  const el  = document.getElementById(id);
  if(!el) return;
  el.textContent  = msg;
  el.style.display = 'block';
  el.className    = `alert ${type}`;
}
function hideAlerts(){
  ['errorMsg','successMsg'].forEach(id=>{
    const el = document.getElementById(id);
    if(el) el.style.display='none';
  });
}

// ── BUTTON LOADING ──
function setLoading(btnId, text=''){
  const btn = document.getElementById(btnId);
  if(!btn) return;
  btn.classList.add('loading');
  btn.dataset.original = btn.innerHTML;
  btn.innerHTML = `<span class="spinner"></span>${text}`;
}
function clearLoading(btnId){
  const btn = document.getElementById(btnId);
  if(!btn) return;
  btn.classList.remove('loading');
  btn.innerHTML = btn.dataset.original || '';
}

// ── PASSWORD STRENGTH ──
function checkStrength(password){
  const fill  = document.getElementById('strengthFill');
  const label = document.getElementById('strengthLabel');
  if(!fill) return;
  let score = 0;
  if(password.length >= 8) score++;
  if(/[A-Z]/.test(password)) score++;
  if(/[0-9]/.test(password)) score++;
  if(/[^A-Za-z0-9]/.test(password)) score++;
  const levels = [
    {w:'0%',   c:'transparent', t:'Enter a password'},
    {w:'25%',  c:'#ff4d6d',     t:'⚠️ Weak'},
    {w:'50%',  c:'#ff9500',     t:'👌 Fair'},
    {w:'75%',  c:'#00d4ff',     t:'✅ Good'},
    {w:'100%', c:'#00f5a0',     t:'🔒 Strong'},
  ];
  const l = levels[score];
  fill.style.width      = l.w;
  fill.style.background = l.c;
  label.textContent     = l.t;
  label.style.color     = l.c;
}

// ── COPY TO CLIPBOARD ──
function copyText(text, btnEl){
  navigator.clipboard.writeText(text);
  const orig = btnEl.textContent;
  btnEl.textContent = '✅ Copied!';
  setTimeout(()=> btnEl.textContent = orig, 2000);
}

// ── SCORE RINGS ──
function renderScores(scores){
  const keys   = ['readability','engagement','seo','length','tone'];
  const labels = ['Readability','Engagement','SEO','Length','Tone'];
  const grid   = document.getElementById('scoresGrid');
  const section= document.getElementById('scoresSection');
  if(!grid) return;

  const R    = 22;
  const CIRC = 2 * Math.PI * R;

  grid.innerHTML = keys.map((k,i)=>{
    const val    = scores[k] || 0;
    const offset = CIRC - (val/100)*CIRC;
    return `<div class="score-item">
      <div class="score-label">${labels[i]}</div>
      <div class="score-ring">
        <svg width="52" height="52" viewBox="0 0 52 52">
          <circle class="track" cx="26" cy="26" r="${R}"/>
          <circle class="fill"  cx="26" cy="26" r="${R}"
            stroke-dasharray="${CIRC}"
            stroke-dashoffset="${offset}"/>
        </svg>
        <div class="score-num">${val}</div>
      </div>
    </div>`;
  }).join('');

  if(scores.suggestion)
    grid.innerHTML += `<div class="score-suggestion">💡 ${scores.suggestion}</div>`;

  section.style.display = 'block';
}

// ── TONE RENDER ──
function renderTone(analysis){
  const grid    = document.getElementById('toneGrid');
  const section = document.getElementById('toneSection');
  if(!grid) return;
  const items = [
    {k:'tone',      l:'Tone'},
    {k:'sentiment', l:'Sentiment'},
    {k:'confidence',l:'Confidence'},
    {k:'summary',   l:'Summary'},
    {k:'improve',   l:'Tip'},
  ];
  grid.innerHTML = items.map(i=>
    `<div class="tone-item">
      <div class="tone-key">${i.l}</div>
      <div class="tone-val">${analysis[i.k]||'—'}</div>
    </div>`
  ).join('');
  section.style.display = 'block';
}

// ── HISTORY RENDER ──
function renderHistory(items){
  const grid = document.getElementById('historyGrid');
  if(!grid) return;

  if(!items.length){
    grid.innerHTML = `<div class="empty">
      <div class="empty-icon">📭</div>
      <div class="empty-title">No content yet</div>
      <div class="empty-sub">Generate content and it will appear here</div>
      <a class="btn btn-primary" style="width:auto;padding:11px 24px;text-decoration:none;display:inline-flex;margin-top:4px;" href="index.html">⚡ Generate Now</a>
    </div>`;
    return;
  }

  grid.innerHTML = items.map((item,i)=>{
    const date = item.created_at
      ? new Date(item.created_at).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})
      : '';
    const safe = (item.output||'').replace(/`/g,'\\`').replace(/\$/g,'\\$');
    return `<div class="history-card" style="animation-delay:${i*0.04}s">
      <div class="card-header">
        <div class="card-meta">
          <span class="tag platform">${item.platform||'—'}</span>
          <span class="tag type">${item.type||'—'}</span>
          <span class="tag lang">${item.language||'en'}</span>
        </div>
        <span class="card-date">${date}</span>
      </div>
      <div class="card-topic">${item.topic||'Untitled'}</div>
      <div class="card-output">${item.output||''}</div>
      <div class="card-footer">
        <span class="tone-badge">🎭 ${item.tone||'professional'}</span>
        <div class="card-actions">
          <button class="btn btn-ghost" onclick="copyText(\`${safe}\`, this)">📋 Copy</button>
          <button class="btn btn-ghost" onclick="reuseItem('${item.topic}','${item.type}','${item.platform}','${item.tone}','${item.language}')">↩ Reuse</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function reuseItem(topic, type, platform, tone, language){
  localStorage.setItem('reuse', JSON.stringify({topic,type,platform,tone,language}));
  window.location.href = 'index.html';
}

document.addEventListener('keydown', e=>{
  if(e.key !== 'Enter') return;
  if(typeof handleLogin    === 'function') handleLogin();
  if(typeof handleRegister === 'function') handleRegister();
});