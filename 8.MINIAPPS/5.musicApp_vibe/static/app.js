// static/app.js - MUSICAPP Frontend Logic with Flask API Integrations

// Application State
const state = {
  currentUser: JSON.parse(sessionStorage.getItem('musicapp_session')) || null,
  musicList: [],
  comments: [],
  notifications: [],
  likes: {}, 
  users: [],
  currentTrackIndex: -1,
  isPlaying: false,
  activeHashtagFilter: "All",
  activeAdminTab: "members",
  activeCommentTarget: null, // musicId
  replyingToCommentId: null // commentId
};

// UI Element Selections
const els = {
  audio: document.getElementById('main-audio-element'),
  headerNav: document.getElementById('header-nav'),
  
  // Views
  pageAuth: document.getElementById('page-auth'),
  pageHome: document.getElementById('page-home'),
  pageTopLike: document.getElementById('page-toplike'),
  pageHashtag: document.getElementById('page-hashtag'),
  pageNotifications: document.getElementById('page-notifications'),
  pageProfile: document.getElementById('page-profile'),
  pageAdmin: document.getElementById('page-admin'),
  
  // Player Controls
  playerCover: document.getElementById('player-song-cover'),
  playerTitle: document.getElementById('player-song-title'),
  playerArtist: document.getElementById('player-song-artist'),
  playerPlayPause: document.getElementById('player-play-pause'),
  playerPlayIcon: document.getElementById('player-play-icon'),
  playerPauseIcon: document.getElementById('player-pause-icon'),
  playerPrev: document.getElementById('player-prev'),
  playerNext: document.getElementById('player-next'),
  playerCurrentTime: document.getElementById('player-current-time'),
  playerTotalTime: document.getElementById('player-total-time'),
  playerProgressTrack: document.getElementById('player-progress-track'),
  playerProgressFill: document.getElementById('player-progress-fill'),
  playerVolumeIcon: document.getElementById('player-volume-icon'),
  playerVolumeTrack: document.getElementById('player-volume-track'),
  playerVolumeFill: document.getElementById('player-volume-fill'),
  playerEq: document.getElementById('player-eq'),
  
  // Detail Modal
  modal: document.getElementById('music-detail-modal'),
  modalClose: document.getElementById('modal-close'),
  modalSongCover: document.getElementById('modal-song-cover'),
  modalSongTitle: document.getElementById('modal-song-title'),
  modalSongArtist: document.getElementById('modal-song-artist'),
  modalSongTags: document.getElementById('modal-song-tags'),
  modalPlayBtn: document.getElementById('modal-play-btn'),
  modalCommentsList: document.getElementById('modal-comments-list'),
  newCommentInput: document.getElementById('new-comment-input'),
  commentSubmitBtn: document.getElementById('comment-submit-btn'),
  
  // Home elements
  homeSearchInput: document.getElementById('home-search-input'),
  homeTopList: document.getElementById('home-top-list'),
  homeHashtagChips: document.getElementById('home-hashtag-chips'),
  homeRecommendedSongs: document.getElementById('home-recommended-songs'),
  goToplikeBtn: document.getElementById('go-toplike-btn'),
  goHashtagBtn: document.getElementById('go-hashtag-btn'),
  
  // TopLike Page elements
  toplikeSearchInput: document.getElementById('toplike-search-input'),
  toplikeChartList: document.getElementById('toplike-chart-list'),
  
  // Hashtag Page elements
  hashtagSearchInput: document.getElementById('hashtag-search-input'),
  hashtagAllChips: document.getElementById('hashtag-all-chips'),
  hashtagSelectedTitle: document.getElementById('hashtag-selected-title'),
  hashtagFilteredList: document.getElementById('hashtag-filtered-list'),
  
  // Notifications elements
  notificationsContainer: document.getElementById('notifications-container'),
  notifClearAll: document.getElementById('notif-clear-all'),
  
  // Profile elements
  profilePicPreview: document.getElementById('profile-pic-preview'),
  profileUsername: document.getElementById('profile-username'),
  profileAvatarSelector: document.getElementById('profile-avatar-selector'),
  formProfileUpdate: document.getElementById('form-profile-update'),
  profileMyComments: document.getElementById('profile-my-comments'),
  
  // Admin elements
  adminMembersList: document.getElementById('admin-members-list'),
  adminSongsList: document.getElementById('admin-songs-list'),
  adminCommentsList: document.getElementById('admin-comments-list'),
  adminAddSongForm: document.getElementById('admin-add-song-form'),
  adminSongTitle: document.getElementById('admin-song-title'),
  adminSongArtist: document.getElementById('admin-song-artist'),
  adminSongCover: document.getElementById('admin-song-cover'),
  adminSongTags: document.getElementById('admin-song-tags')
};

// Avatar Pool
const AVATARS = {
  avatar1: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&q=80",
  avatar2: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&q=80",
  avatar3: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&q=80",
  avatar4: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&q=80",
  admin: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&q=80"
};

// Global Fetch Wrapper
async function apiCall(url, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  try {
    const res = await fetch(url, options);
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || 'API request failed');
    }
    return data;
  } catch (err) {
    console.error(`API Error for ${url}:`, err);
    throw err;
  }
}

// Initialize App
async function initApp() {
  await loadMusicList();
  if (state.currentUser) {
    await refreshUserData();
  }
  renderNavigation();
  navigateTo('page-home');
  setupEventListeners();
  initAudioPlayer();
  
  // Periodic poll of notifications (every 8 seconds to fetch dynamic notifications generated by simulated bots/replies)
  setInterval(pollNotifications, 8000);
}

// Load dynamic data from Flask API
async function loadMusicList() {
  try {
    state.musicList = await apiCall('/api/music');
  } catch (err) {
    console.error("Failed to load music list:", err);
  }
}

async function refreshUserData() {
  if (!state.currentUser) return;
  try {
    // Refresh user's notifications
    state.notifications = await apiCall(`/api/notifications/${state.currentUser.id}`);
  } catch (err) {
    console.error("Failed to refresh user data:", err);
  }
}

async function pollNotifications() {
  if (!state.currentUser || state.currentUser.role === 'admin') return;
  try {
    const freshNotifs = await apiCall(`/api/notifications/${state.currentUser.id}`);
    const unreadBefore = state.notifications.filter(n => !n.read).length;
    const unreadAfter = freshNotifs.filter(n => !n.read).length;
    
    state.notifications = freshNotifs;
    
    if (unreadAfter !== unreadBefore) {
      renderNavigation();
      if (state.currentView === 'page-notifications') {
        renderNotificationsPage();
      }
    }
  } catch (err) {
    console.warn("Poll notifications failed:", err);
  }
}

// Render dynamic top bar links
function renderNavigation() {
  const isLogged = !!state.currentUser;
  const isAdmin = isLogged && state.currentUser.role === 'admin';
  
  let unreadCount = 0;
  if (isLogged) {
    unreadCount = state.notifications.filter(n => n.recipientId === state.currentUser.id && !n.read).length;
  }
  
  let html = `
    <li><a class="nav-item" data-page="page-home">HOME</a></li>
    <li><a class="nav-item" data-page="page-toplike">TOPLIKE</a></li>
    <li><a class="nav-item" data-page="page-hashtag">HASHTAG</a></li>
  `;
  
  if (isLogged) {
    if (isAdmin) {
      html += `
        <li><a class="nav-item" data-page="page-admin">ADMIN 콘솔</a></li>
      `;
    } else {
      html += `
        <li>
          <a class="nav-item" data-page="page-notifications">
            NOTIFICATIONS
            ${unreadCount > 0 ? `<span class="badge">${unreadCount}</span>` : ''}
          </a>
        </li>
        <li>
          <a class="nav-item" data-page="page-profile" style="display:flex; align-items:center; gap:8px;">
            <img class="nav-profile-pic" src="${AVATARS[state.currentUser.avatar] || AVATARS.avatar1}" alt="Avatar">
            PROFILE (${state.currentUser.username})
          </a>
        </li>
      `;
    }
    html += `<li><a class="nav-item" id="btn-logout">LOGOUT</a></li>`;
  } else {
    html += `<li><a class="nav-item" data-page="page-auth">LOGIN</a></li>`;
  }
  
  els.headerNav.innerHTML = html;
  
  // Highlight active menu link
  const items = els.headerNav.querySelectorAll('.nav-item');
  items.forEach(item => {
    const targetPage = item.getAttribute('data-page');
    if (targetPage === state.currentView) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
  
  // Re-bind click events for navigation
  els.headerNav.querySelectorAll('[data-page]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      navigateTo(el.getAttribute('data-page'));
    });
  });
  
  const logoutBtn = document.getElementById('btn-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', handleLogout);
  }
}

// Router Control
async function navigateTo(pageId) {
  state.currentView = pageId;
  
  // Hide all sections
  [els.pageAuth, els.pageHome, els.pageTopLike, els.pageHashtag, els.pageNotifications, els.pageProfile, els.pageAdmin]
    .forEach(el => el.classList.remove('active'));
  
  if (state.currentUser) {
    await refreshUserData();
  }
  
  // Render correct page contents
  if (pageId === 'page-home') {
    els.pageHome.classList.add('active');
    await loadMusicList();
    renderHomePage();
  } else if (pageId === 'page-toplike') {
    els.pageTopLike.classList.add('active');
    await loadMusicList();
    renderTopLikePage();
  } else if (pageId === 'page-hashtag') {
    els.pageHashtag.classList.add('active');
    await loadMusicList();
    renderHashtagPage();
  } else if (pageId === 'page-notifications') {
    if (!requireLogin()) return;
    els.pageNotifications.classList.add('active');
    renderNotificationsPage();
  } else if (pageId === 'page-profile') {
    if (!requireLogin()) return;
    els.pageProfile.classList.add('active');
    renderProfilePage();
  } else if (pageId === 'page-admin') {
    if (!requireLogin()) return;
    if (state.currentUser.role !== 'admin') {
      alert("관리자 권한이 없습니다.");
      navigateTo('page-home');
      return;
    }
    els.pageAdmin.classList.add('active');
    renderAdminPage();
  } else if (pageId === 'page-auth') {
    els.pageAuth.classList.add('active');
    showAuthView('login');
  }
  
  renderNavigation();
}

function requireLogin() {
  if (!state.currentUser) {
    alert("이 기능을 사용하려면 로그인이 필요합니다.");
    navigateTo('page-auth');
    return false;
  }
  return true;
}

// Switch between Login and Register views
function showAuthView(view) {
  const loginView = document.getElementById('auth-login-view');
  const registerView = document.getElementById('auth-register-view');
  if (view === 'login') {
    loginView.style.display = 'block';
    registerView.style.display = 'none';
  } else {
    loginView.style.display = 'none';
    registerView.style.display = 'block';
  }
}

// Event Listeners setup
function setupEventListeners() {
  // Logo redirect
  document.getElementById('nav-logo').addEventListener('click', () => navigateTo('page-home'));
  
  // Auth Form Toggles
  document.getElementById('go-register').addEventListener('click', () => showAuthView('register'));
  document.getElementById('go-login').addEventListener('click', () => showAuthView('login'));
  
  // Login Submitting
  document.getElementById('form-login').addEventListener('submit', handleLoginSubmit);
  // Register Submitting
  document.getElementById('form-register').addEventListener('submit', handleRegisterSubmit);
  
  // Home view redirects
  els.goToplikeBtn.addEventListener('click', () => navigateTo('page-toplike'));
  els.goHashtagBtn.addEventListener('click', () => navigateTo('page-hashtag'));
  
  // Search filtering inputs
  els.homeSearchInput.addEventListener('input', (e) => {
    const val = e.target.value.trim().toLowerCase();
    renderHomePage(val);
  });
  
  els.toplikeSearchInput.addEventListener('input', (e) => {
    const val = e.target.value.trim().toLowerCase();
    renderTopLikePage(val);
  });
  
  els.hashtagSearchInput.addEventListener('input', (e) => {
    const val = e.target.value.trim().toLowerCase();
    renderHashtagPage(val);
  });
  
  // Modal Close
  els.modalClose.addEventListener('click', () => {
    els.modal.classList.remove('active');
    state.activeCommentTarget = null;
  });
  els.modal.addEventListener('click', (e) => {
    if (e.target === els.modal) {
      els.modal.classList.remove('active');
      state.activeCommentTarget = null;
    }
  });
  
  // Modal Comment Actions
  els.commentSubmitBtn.addEventListener('click', submitNewComment);
  els.newCommentInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') submitNewComment();
  });
  
  // Modal Quick Play
  els.modalPlayBtn.addEventListener('click', () => {
    if (state.activeCommentTarget) {
      const idx = state.musicList.findIndex(m => m.id === state.activeCommentTarget);
      if (idx !== -1) playTrack(idx);
    }
  });
  
  // Profile update
  els.formProfileUpdate.addEventListener('submit', handleProfileUpdate);
  
  // Notifications Page
  els.notifClearAll.addEventListener('click', clearAllNotifications);
  
  // Admin Tabs switching
  document.querySelectorAll('.admin-tab').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.admin-tab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.admin-tab-content').forEach(c => c.classList.remove('active'));
      
      const tabName = btn.getAttribute('data-tab');
      btn.classList.add('active');
      document.getElementById(`admin-tab-${tabName}`).classList.add('active');
      state.activeAdminTab = tabName;
      renderAdminPage();
    });
  });
  
  // Admin add song
  els.adminAddSongForm.addEventListener('submit', handleAdminAddSong);
}

/* AUTHENTICATION HANDLERS */
async function handleLoginSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('login-id').value.trim();
  const pw = document.getElementById('login-pw').value.trim();
  
  try {
    const res = await apiCall('/api/auth/login', 'POST', { id, password: pw });
    if (res.success) {
      state.currentUser = res.user;
      sessionStorage.setItem('musicapp_session', JSON.stringify(res.user));
      alert(`${res.user.username}님, 환영합니다!`);
      
      document.getElementById('form-login').reset();
      
      if (res.user.role === 'admin') {
        navigateTo('page-admin');
      } else {
        navigateTo('page-home');
      }
    }
  } catch (err) {
    alert(err.message || "로그인 실패");
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const id = document.getElementById('reg-id').value.trim();
  const name = document.getElementById('reg-name').value.trim();
  const pw = document.getElementById('reg-pw').value.trim();
  
  try {
    const res = await apiCall('/api/auth/register', 'POST', { id, username: name, password: pw });
    if (res.success) {
      alert(res.message || "회원가입 성공!");
      document.getElementById('form-register').reset();
      showAuthView('login');
    }
  } catch (err) {
    alert(err.message || "회원가입 실패");
  }
}

function handleLogout() {
  state.currentUser = null;
  sessionStorage.removeItem('musicapp_session');
  alert("로그아웃 되었습니다.");
  navigateTo('page-home');
}

/* HOME PAGE RENDERING */
function renderHomePage(filterQuery = "") {
  // Sort songs by likes descending for 인기 차트 (ranking list)
  const rankedMusic = [...state.musicList].sort((a, b) => b.likes - a.likes);
  
  // Render TOP 10 Ranking
  const top10 = rankedMusic.slice(0, 10);
  let topListHtml = "";
  
  top10.forEach((music, i) => {
    // Check if current user liked this music
    // We will check by fetching likes status, or we can look up if user exists.
    // To make it stateless, app.py stores a likes map, but let's query the likes array directly.
    // In our python code, `db["likes"][user_id]` is a list of musicIds.
    // We can fetch user likes list. However, to save network bandwidth, 
    // let's assume we can just check if state.likes has it. Since state.likes is loaded dynamically, 
    // we can request it, or check if user id likes includes this ID.
    // Wait, let's request user likes from session or back-end. Actually, we can fetch all details in loadMusicList or when user logs in.
    // To simplify: we can check if the song is liked by checking if it exists in window.likedTracks.
    // Let's implement likedTracks cache in sessionStorage or fetch it.
    const isLiked = isTrackLikedByUser(music.id);
    
    topListHtml += `
      <div class="rank-item" data-id="${music.id}">
        <div class="rank-num">${i + 1}</div>
        <img class="song-cover" src="${music.cover}" alt="Album Art">
        <div class="song-info">
          <div class="song-title" onclick="window.openDetailModal('${music.id}')">${escapeHtml(music.title)}</div>
          <div class="song-artist">${escapeHtml(music.artist)}</div>
        </div>
        <div class="song-meta">
          <div class="like-action ${isLiked ? 'liked' : ''}" onclick="window.toggleLike('${music.id}')">
            <svg class="icon-svg" viewBox="0 0 24 24">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            <span>${music.likes}</span>
          </div>
          <div class="btn-mini" style="font-size:11px; padding:4px 8px; cursor:pointer;" onclick="window.openDetailModal('${music.id}')">
            💬 의견 보기
          </div>
          <button class="btn-mini" onclick="window.playTrackById('${music.id}')">▶</button>
        </div>
      </div>
    `;
  });
  
  els.homeTopList.innerHTML = topListHtml || `<div class="empty-state">차트에 음악이 없습니다.</div>`;
  
  // Render Recommended Categories Chips
  const allTags = new Set(["All"]);
  state.musicList.forEach(m => {
    if (m.tags) m.tags.forEach(t => allTags.add(t));
  });
  
  let chipHtml = "";
  allTags.forEach(tag => {
    const isActive = state.activeHashtagFilter === tag;
    chipHtml += `
      <div class="chip ${isActive ? 'active' : ''}" onclick="window.selectHomeHashtag('${escapeHtml(tag)}')">
        #${escapeHtml(tag)}
      </div>
    `;
  });
  els.homeHashtagChips.innerHTML = chipHtml;
  
  // Filter Recommended lists based on active Tag AND search query
  let filteredRecs = state.musicList;
  if (state.activeHashtagFilter !== "All") {
    filteredRecs = filteredRecs.filter(m => m.tags && m.tags.includes(state.activeHashtagFilter));
  }
  
  if (filterQuery) {
    filteredRecs = filteredRecs.filter(m => 
      m.title.toLowerCase().includes(filterQuery) || 
      m.artist.toLowerCase().includes(filterQuery) || 
      (m.tags && m.tags.some(t => t.toLowerCase().includes(filterQuery)))
    );
  }
  
  // Render recommendation list (max 8)
  let recsHtml = "";
  filteredRecs.slice(0, 8).forEach(music => {
    const isLiked = isTrackLikedByUser(music.id);
    recsHtml += `
      <div class="rank-item" data-id="${music.id}">
        <img class="song-cover" src="${music.cover}" alt="Album Art">
        <div class="song-info">
          <div class="song-title" onclick="window.openDetailModal('${music.id}')">${escapeHtml(music.title)}</div>
          <div class="song-artist">${escapeHtml(music.artist)}</div>
          <div class="hashtag-display-area">
            ${(music.tags || []).map(t => `<span class="tag-badge">#${escapeHtml(t)}</span>`).join('')}
          </div>
        </div>
        <div class="song-meta">
          <div class="like-action ${isLiked ? 'liked' : ''}" onclick="window.toggleLike('${music.id}')">
            <svg class="icon-svg" viewBox="0 0 24 24">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            <span>${music.likes}</span>
          </div>
          <button class="btn-mini" onclick="window.playTrackById('${music.id}')">▶</button>
        </div>
      </div>
    `;
  });
  
  els.homeRecommendedSongs.innerHTML = recsHtml || `<div class="empty-state">해당 태그/조건에 부합하는 노래가 없습니다.</div>`;
}

function isTrackLikedByUser(musicId) {
  if (!state.currentUser) return false;
  // Cache user likes locally in sessionStorage under a prefix for quick lookup
  const userLikes = JSON.parse(sessionStorage.getItem(`musicapp_likes_${state.currentUser.id}`)) || [];
  return userLikes.includes(musicId);
}

function saveTrackLikeState(musicId, isLiked) {
  if (!state.currentUser) return;
  const key = `musicapp_likes_${state.currentUser.id}`;
  let userLikes = JSON.parse(sessionStorage.getItem(key)) || [];
  if (isLiked) {
    if (!userLikes.includes(musicId)) userLikes.push(musicId);
  } else {
    userLikes = userLikes.filter(id => id !== musicId);
  }
  sessionStorage.setItem(key, JSON.stringify(userLikes));
}

window.selectHomeHashtag = function(tag) {
  state.activeHashtagFilter = tag;
  renderHomePage();
};

window.playTrackById = function(musicId) {
  const idx = state.musicList.findIndex(m => m.id === musicId);
  if (idx !== -1) playTrack(idx);
};

/* TOPLIKE PAGE RENDERING */
function renderTopLikePage(filterQuery = "") {
  let rankedMusic = [...state.musicList].sort((a, b) => b.likes - a.likes);
  
  if (filterQuery) {
    rankedMusic = rankedMusic.filter(m => 
      m.title.toLowerCase().includes(filterQuery) ||
      m.artist.toLowerCase().includes(filterQuery)
    );
  }
  
  let chartHtml = "";
  rankedMusic.forEach((music, i) => {
    const isLiked = isTrackLikedByUser(music.id);
    
    chartHtml += `
      <div class="rank-item" data-id="${music.id}">
        <div class="rank-num">${i + 1}</div>
        <img class="song-cover" src="${music.cover}" alt="Album Art">
        <div class="song-info">
          <div class="song-title" onclick="window.openDetailModal('${music.id}')">${escapeHtml(music.title)}</div>
          <div class="song-artist">${escapeHtml(music.artist)}</div>
          <div class="hashtag-display-area">
            ${(music.tags || []).map(t => `<span class="tag-badge">#${escapeHtml(t)}</span>`).join('')}
          </div>
        </div>
        <div class="song-meta">
          <div class="like-action ${isLiked ? 'liked' : ''}" onclick="window.toggleLike('${music.id}')">
            <svg class="icon-svg" viewBox="0 0 24 24">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            <span>${music.likes}</span>
          </div>
          <div class="btn-mini" style="font-size:11px; padding:4px 8px; cursor:pointer;" onclick="window.openDetailModal('${music.id}')">
            💬 의견 보기
          </div>
          <button class="btn-mini" onclick="window.playTrackById('${music.id}')">▶</button>
        </div>
      </div>
    `;
  });
  
  els.toplikeChartList.innerHTML = chartHtml || `<div class="empty-state">조건에 부합하는 음악이 없습니다.</div>`;
}

/* HASHTAG PAGE RENDERING */
function renderHashtagPage(filterQuery = "") {
  // Collect all hashtags
  const allTags = new Set();
  state.musicList.forEach(m => {
    if (m.tags) m.tags.forEach(t => allTags.add(t));
  });
  
  let tagsHtml = "";
  allTags.forEach(tag => {
    tagsHtml += `
      <span class="chip" onclick="window.filterHashtagPage('${escapeHtml(tag)}')">#${escapeHtml(tag)}</span>
    `;
  });
  els.hashtagAllChips.innerHTML = tagsHtml || `<div style="color:var(--color-text-muted); font-size:12px;">등록된 태그가 없습니다.</div>`;
  
  // Render songs with tag inputs
  let list = state.musicList;
  if (filterQuery) {
    list = list.filter(m => 
      m.title.toLowerCase().includes(filterQuery) ||
      m.artist.toLowerCase().includes(filterQuery) ||
      (m.tags && m.tags.some(t => t.toLowerCase().includes(filterQuery)))
    );
  }
  
  let listHtml = "";
  list.forEach(music => {
    const isLiked = isTrackLikedByUser(music.id);
    listHtml += `
      <div class="rank-item" style="align-items:flex-start; padding:15px;">
        <img class="song-cover" src="${music.cover}" alt="Cover" style="width:55px; height:55px;">
        <div class="song-info">
          <div class="song-title" style="font-size:15px;" onclick="window.openDetailModal('${music.id}')">${escapeHtml(music.title)}</div>
          <div class="song-artist" style="margin-bottom:8px;">${escapeHtml(music.artist)}</div>
          
          <div class="hashtag-display-area" id="hashtag-list-${music.id}">
            ${(music.tags || []).map(t => `
              <span class="tag-badge" style="background:rgba(236,72,153,0.06); border-color:rgba(236,72,153,0.15); color:#F472B6;">
                #${escapeHtml(t)}
              </span>
            `).join('')}
            
            <div class="add-tag-box">
              <input type="text" placeholder="태그 추가" id="tag-input-${music.id}" onkeydown="window.handleAddTagKeydown(event, '${music.id}')">
              <button onclick="window.submitAddTag('${music.id}')">+</button>
            </div>
          </div>
        </div>
        <div class="song-meta" style="align-self: center;">
          <div class="like-action ${isLiked ? 'liked' : ''}" onclick="window.toggleLike('${music.id}')">
            <svg class="icon-svg" viewBox="0 0 24 24">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            <span>${music.likes}</span>
          </div>
          <button class="btn-mini" onclick="window.playTrackById('${music.id}')">▶</button>
        </div>
      </div>
    `;
  });
  
  els.hashtagFilteredList.innerHTML = listHtml || `<div class="empty-state">조건에 부합하는 음악이 없습니다.</div>`;
}

window.filterHashtagPage = function(tag) {
  els.hashtagSearchInput.value = tag;
  renderHashtagPage(tag.toLowerCase());
  els.hashtagSelectedTitle.innerText = `'#${tag}' 태그 검색 결과`;
};

window.handleAddTagKeydown = function(e, musicId) {
  if (e.key === 'Enter') {
    window.submitAddTag(musicId);
  }
};

async function submitAddTagAPI(musicId, tag) {
  try {
    const res = await apiCall(`/api/music/${musicId}/tag`, 'POST', { tag });
    if (res.success) {
      // Update local item
      const track = state.musicList.find(m => m.id === musicId);
      if (track) {
        track.tags = res.tags;
      }
      return true;
    }
  } catch (err) {
    alert(err.message || "태그 추가 실패");
  }
  return false;
}

window.submitAddTag = async function(musicId) {
  if (!state.currentUser) {
    alert("해시태그를 추가하려면 로그인이 필요합니다.");
    navigateTo('page-auth');
    return;
  }
  
  const input = document.getElementById(`tag-input-${musicId}`);
  let newTag = input.value.trim().replace(/^#/, ""); 
  if (!newTag) return;
  
  const success = await submitAddTagAPI(musicId, newTag);
  if (success) {
    input.value = "";
    renderHashtagPage(els.hashtagSearchInput.value.trim().toLowerCase());
    
    // Refresh modal details tags
    if (state.activeCommentTarget === musicId) {
      const track = state.musicList.find(m => m.id === musicId);
      if (track) renderModalDetail(track);
    }
  }
};

/* LIKES CONTROLLER */
window.toggleLike = async function(musicId) {
  if (!state.currentUser) {
    alert("좋아요는 로그인 후 이용 가능합니다.");
    navigateTo('page-auth');
    return;
  }
  
  try {
    const res = await apiCall(`/api/music/${musicId}/like`, 'POST', { userId: state.currentUser.id });
    if (res.success) {
      const trackIndex = state.musicList.findIndex(m => m.id === musicId);
      if (trackIndex !== -1) {
        state.musicList[trackIndex].likes = res.likes;
      }
      
      const isLikedNow = res.action === 'like';
      saveTrackLikeState(musicId, isLikedNow);
      
      // Refresh current active view
      if (state.currentView === 'page-home') renderHomePage(els.homeSearchInput.value.trim().toLowerCase());
      if (state.currentView === 'page-toplike') renderTopLikePage(els.toplikeSearchInput.value.trim().toLowerCase());
      if (state.currentView === 'page-hashtag') renderHashtagPage(els.hashtagSearchInput.value.trim().toLowerCase());
    }
  } catch (err) {
    alert(err.message || "좋아요 작업 실패");
  }
};

/* NOTIFICATIONS PAGE RENDERING */
function renderNotificationsPage() {
  const notifs = state.notifications
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
  let html = "";
  notifs.forEach(n => {
    const isUnread = !n.read;
    html += `
      <div class="notif-item ${isUnread ? 'unread' : ''}">
        <div class="notif-main">
          <div class="notif-badge ${n.type}">
            ${n.type === 'like' ? '❤️' : '💬'}
          </div>
          <div class="notif-text">
            <span class="notif-sender">${escapeHtml(n.senderName)}</span>님이 
            <span class="notif-music" onclick="window.openDetailModal('${n.musicId}')">'${escapeHtml(n.musicTitle)}'</span> 음원 댓글에 
            ${n.type === 'like' ? '좋아요를 눌렀습니다.' : '대댓글을 달았습니다.'}
            <span class="notif-preview">"${escapeHtml(n.content)}"</span>
          </div>
        </div>
        <div class="notif-right">
          <span class="notif-time">${formatDate(n.timestamp)}</span>
          <div class="notif-action-btns">
            ${isUnread ? `<button class="btn-mini" onclick="window.markNotifRead('${n.id}')">읽음</button>` : ''}
            <button class="btn-mini" onclick="window.deleteNotif('${n.id}')">삭제</button>
          </div>
        </div>
      </div>
    `;
  });
  
  els.notificationsContainer.innerHTML = html || `<div class="empty-state">새로운 알림이 없습니다.</div>`;
  renderNavigation(); 
}

window.markNotifRead = async function(id) {
  try {
    const res = await apiCall(`/api/notifications/${id}/read`, 'POST');
    if (res.success) {
      const notif = state.notifications.find(n => n.id === id);
      if (notif) notif.read = true;
      renderNotificationsPage();
    }
  } catch (err) {
    console.error("Mark read failed:", err);
  }
};

window.deleteNotif = async function(id) {
  // Clear dynamically from notifications array by reading them or updating state.
  // In Flask we can delete or mark read. Let's just update local view since Flask /api/notifications API allows loading/purging.
  // Wait, let's look at the Flask deletion API: DELETE /api/notifications/<user_id> clears all.
  // Let's implement individual notification removal by just marking it as deleted in UI or filtering it.
  state.notifications = state.notifications.filter(n => n.id !== id);
  renderNotificationsPage();
};

async function clearAllNotifications() {
  if (confirm("모든 알림을 삭제 및 읽음 처리 하시겠습니까?")) {
    try {
      const res = await apiCall(`/api/notifications/${state.currentUser.id}`, 'DELETE');
      if (res.success) {
        state.notifications = [];
        renderNotificationsPage();
      }
    } catch (err) {
      alert("알림 삭제 실패");
    }
  }
}

/* PROFILE PAGE RENDERING */
async function renderProfilePage() {
  els.profilePicPreview.src = AVATARS[state.currentUser.avatar] || AVATARS.avatar1;
  els.profileUsername.value = state.currentUser.username;
  
  // Render avatar selector
  let selectorHtml = "";
  Object.keys(AVATARS).forEach(key => {
    if (key === 'admin' && state.currentUser.role !== 'admin') return; 
    
    const isSelected = state.currentUser.avatar === key;
    selectorHtml += `
      <img class="avatar-option ${isSelected ? 'selected' : ''}" 
           src="${AVATARS[key]}" 
           onclick="window.selectProfileAvatar('${key}')" 
           alt="${key}">
    `;
  });
  els.profileAvatarSelector.innerHTML = selectorHtml;
  
  // Render user comments list from backend
  await renderProfileCommentsList();
}

window.selectProfileAvatar = function(avatarKey) {
  state.currentUser.avatar = avatarKey;
  const options = els.profileAvatarSelector.querySelectorAll('.avatar-option');
  options.forEach(opt => {
    if (opt.getAttribute('alt') === avatarKey) {
      opt.classList.add('selected');
    } else {
      opt.classList.remove('selected');
    }
  });
  els.profilePicPreview.src = AVATARS[avatarKey];
};

async function renderProfileCommentsList() {
  try {
    const userComments = await apiCall(`/api/profile/comments/${state.currentUser.id}`);
    let html = "";
    
    userComments.forEach(c => {
      const music = state.musicList.find(m => m.id === c.musicId);
      const musicTitle = music ? music.title : "알 수 없는 음원";
      const isReply = !!c.parentId;
      
      html += `
        <div class="my-comment-item">
          <div class="my-comment-music">${isReply ? '[대댓글]' : '[댓글]'} ${escapeHtml(musicTitle)}</div>
          <div class="my-comment-text">${escapeHtml(c.content)}</div>
          <div style="font-size:10px; color:var(--color-text-muted);">${formatDate(c.timestamp)}</div>
          <button class="my-comment-delete" onclick="window.deleteProfileComment('${c.id}')" title="삭제">
            <svg class="icon-svg" viewBox="0 0 24 24" style="width:16px; height:16px;">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
      `;
    });
    
    els.profileMyComments.innerHTML = html || `<div class="empty-state">작성한 댓글이 없습니다.</div>`;
  } catch (err) {
    console.error("Comments fetch failed:", err);
  }
}

window.deleteProfileComment = async function(commentId) {
  if (confirm("댓글을 정말 삭제하시겠습니까?")) {
    try {
      const res = await apiCall(`/api/comments/${commentId}`, 'DELETE');
      if (res.success) {
        await renderProfileCommentsList();
      }
    } catch (err) {
      alert("댓글 삭제 실패");
    }
  }
};

async function handleProfileUpdate(e) {
  e.preventDefault();
  const newName = els.profileUsername.value.trim();
  if (!newName) return;
  
  try {
    const res = await apiCall('/api/profile', 'POST', {
      userId: state.currentUser.id,
      username: newName,
      avatar: state.currentUser.avatar
    });
    if (res.success) {
      state.currentUser = res.user;
      sessionStorage.setItem('musicapp_session', JSON.stringify(res.user));
      alert("프로필 정보가 저장되었습니다.");
      renderNavigation();
    }
  } catch (err) {
    alert(err.message || "프로필 저장 실패");
  }
}

/* MUSIC DETAIL MODAL & COMMENTS (SNS) CONTROLLER */
window.openDetailModal = async function(musicId) {
  const track = state.musicList.find(m => m.id === musicId);
  if (!track) return;
  
  state.activeCommentTarget = musicId;
  els.modal.classList.add('active');
  
  renderModalDetail(track);
  await loadAndRenderModalComments(musicId);
};

function renderModalDetail(track) {
  els.modalSongCover.src = track.cover;
  els.modalSongTitle.innerText = track.title;
  els.modalSongArtist.innerText = track.artist;
  
  let tagsHtml = "";
  if (track.tags && track.tags.length > 0) {
    tagsHtml = track.tags.map(t => `<span class="tag-badge" style="cursor:pointer;" onclick="window.clickModalTag('${escapeHtml(t)}')">#${escapeHtml(t)}</span>`).join('');
  }
  els.modalSongTags.innerHTML = tagsHtml || `<span style="font-size:11px; color:var(--color-text-muted)">태그 없음</span>`;
}

window.clickModalTag = function(tag) {
  els.modal.classList.remove('active');
  state.activeCommentTarget = null;
  navigateTo('page-hashtag');
  window.filterHashtagPage(tag);
};

async function loadAndRenderModalComments(musicId) {
  try {
    const commentsList = await apiCall(`/api/comments/${musicId}`);
    
    // Filter core comments (no parentId)
    const coreComments = commentsList.filter(c => !c.parentId);
    
    let html = "";
    coreComments.forEach(c => {
      const isCommentLiked = state.currentUser ? (c.likes || []).includes(state.currentUser.id) : false;
      const likesCount = (c.likes || []).length;
      
      const replies = commentsList.filter(r => r.parentId === c.id);
      
      let repliesHtml = "";
      replies.forEach(r => {
        const isReplyLiked = state.currentUser ? (r.likes || []).includes(state.currentUser.id) : false;
        const rLikesCount = (r.likes || []).length;
        
        repliesHtml += `
          <div class="comment-node" style="margin-bottom: 6px; background: rgba(255,255,255,0.015);">
            <div class="comment-header">
              <img class="comment-avatar" src="${AVATARS[r.avatar] || AVATARS.avatar1}" alt="Avatar">
              <span class="comment-user">${escapeHtml(r.username)}</span>
              <span class="comment-time">${formatDate(r.timestamp)}</span>
            </div>
            <div class="comment-content">${escapeHtml(r.content)}</div>
            <div class="comment-actions">
              <span class="comment-action-btn ${isReplyLiked ? 'liked' : ''}" onclick="window.likeComment('${r.id}')">
                ❤️ <span>${rLikesCount}</span>
              </span>
            </div>
          </div>
        `;
      });
      
      html += `
        <div class="comment-node" style="border: 1px solid rgba(255,255,255,0.06);">
          <div class="comment-header">
            <img class="comment-avatar" src="${AVATARS[c.avatar] || AVATARS.avatar1}" alt="Avatar">
            <span class="comment-user">${escapeHtml(c.username)}</span>
            <span class="comment-time">${formatDate(c.timestamp)}</span>
          </div>
          <div class="comment-content">${escapeHtml(c.content)}</div>
          
          <div class="comment-actions">
            <span class="comment-action-btn ${isCommentLiked ? 'liked' : ''}" onclick="window.likeComment('${c.id}')">
              ❤️ <span>${likesCount}</span>
            </span>
            <span class="comment-action-btn" onclick="window.toggleReplyInput('${c.id}')">
              💬 답글 달기
            </span>
          </div>
          
          <div class="comment-replies" id="replies-box-${c.id}">
            ${repliesHtml}
          </div>
          
          <div class="reply-input-box" id="reply-box-${c.id}" style="display: none;">
            <input type="text" placeholder="대댓글을 입력하세요..." id="reply-input-${c.id}">
            <button onclick="window.submitReply('${c.id}')">등록</button>
          </div>
        </div>
      `;
    });
    
    els.modalCommentsList.innerHTML = html || `<div class="empty-state">아직 남겨진 의견이 없습니다. 첫 의견을 남겨보세요!</div>`;
  } catch (err) {
    console.error("Comments render error:", err);
  }
}

// Comments submissions
async function submitNewComment() {
  if (!state.currentUser) {
    alert("댓글을 달려면 로그인이 필요합니다.");
    navigateTo('page-auth');
    els.modal.classList.remove('active');
    return;
  }
  
  const content = els.newCommentInput.value.trim();
  if (!content) return;
  
  try {
    const res = await apiCall('/api/comments', 'POST', {
      musicId: state.activeCommentTarget,
      userId: state.currentUser.id,
      username: state.currentUser.username,
      avatar: state.currentUser.avatar,
      content: content
    });
    
    if (res.success) {
      els.newCommentInput.value = "";
      await loadAndRenderModalComments(state.activeCommentTarget);
      
      // Trigger bot reaction comment trigger (simulate bot reply from Python flask or locally after 3.5s)
      triggerLocalCommentBot(state.activeCommentTarget, res.comment);
    }
  } catch (err) {
    alert(err.message || "의견 등록 실패");
  }
}

window.toggleReplyInput = function(commentId) {
  const box = document.getElementById(`reply-box-${commentId}`);
  if (box.style.display === 'none') {
    box.style.display = 'flex';
    document.getElementById(`reply-input-${commentId}`).focus();
  } else {
    box.style.display = 'none';
  }
};

window.submitReply = async function(parentCommentId) {
  if (!state.currentUser) {
    alert("대댓글 작성을 위해 로그인이 필요합니다.");
    navigateTo('page-auth');
    els.modal.classList.remove('active');
    return;
  }
  
  const input = document.getElementById(`reply-input-${parentCommentId}`);
  const content = input.value.trim();
  if (!content) return;
  
  try {
    const res = await apiCall('/api/comments', 'POST', {
      musicId: state.activeCommentTarget,
      userId: state.currentUser.id,
      username: state.currentUser.username,
      avatar: state.currentUser.avatar,
      content: content,
      parentId: parentCommentId
    });
    
    if (res.success) {
      input.value = "";
      document.getElementById(`reply-box-${parentCommentId}`).style.display = 'none';
      await loadAndRenderModalComments(state.activeCommentTarget);
    }
  } catch (err) {
    alert(err.message || "대댓글 등록 실패");
  }
};

window.likeComment = async function(commentId) {
  if (!state.currentUser) {
    alert("좋아요는 로그인이 필요합니다.");
    navigateTo('page-auth');
    els.modal.classList.remove('active');
    return;
  }
  
  try {
    const res = await apiCall(`/api/comments/${commentId}/like`, 'POST', {
      userId: state.currentUser.id,
      username: state.currentUser.username
    });
    if (res.success) {
      await loadAndRenderModalComments(state.activeCommentTarget);
    }
  } catch (err) {
    alert("댓글 좋아요 반영 실패");
  }
};

/* BOT SIMULATION TRIGGER IN CLIENT */
function triggerLocalCommentBot(musicId, comment) {
  setTimeout(async () => {
    if (comment.userId.startsWith("user")) return; 
    
    const botReplies = [
      "저도 이 노래 앨범 전체 다 들어봤는데 정말 강추해요! 🔥",
      "의견 공감합니다! 플레이리스트에 추가해뒀어요.",
      "이 곡 도입부 멜로디가 너무 중독성 넘치는 것 같아용~",
      "추천 태그 보고 들었는데 완전 좋은데요?! 🎧",
      "오늘도 이 노래 무한반복 중입니다!"
    ];
    const randomReply = botReplies[Math.floor(Math.random() * botReplies.length)];
    
    try {
      // Submit a comment reply on behalf of user2 (MelodyQueen)
      await apiCall('/api/comments', 'POST', {
        musicId: musicId,
        userId: "user2",
        username: "MelodyQueen",
        avatar: "avatar2",
        content: randomReply,
        parentId: comment.id
      });
      
      // If modal remains active, refresh
      if (els.modal.classList.contains('active') && state.activeCommentTarget === musicId) {
        await loadAndRenderModalComments(musicId);
      }
      
      // Pull fresh notifications badge
      await pollNotifications();
    } catch (err) {
      console.warn("Local bot reply trigger failed:", err);
    }
  }, 3500);
}

/* ADMIN PANEL RENDERING */
async function renderAdminPage() {
  if (state.activeAdminTab === 'members') {
    await renderAdminMembers();
  } else if (state.activeAdminTab === 'songs') {
    await renderAdminSongs();
  } else if (state.activeAdminTab === 'comments') {
    await renderAdminComments();
  }
}

async function renderAdminMembers() {
  try {
    const users = await apiCall('/api/admin/users');
    let html = "";
    users.forEach(u => {
      const isBlocked = u.status === 'blocked';
      const isAdmin = u.role === 'admin';
      
      html += `
        <tr>
          <td><strong>${escapeHtml(u.id)}</strong></td>
          <td>${escapeHtml(u.username)}</td>
          <td>
            <span class="status-badge ${isBlocked ? 'blocked' : 'active'}">
              ${isBlocked ? '이용 정지' : '정상'}
            </span>
          </td>
          <td>${isAdmin ? '관리자' : '일반 회원'}</td>
          <td class="admin-actions">
            ${!isAdmin ? `
              <button class="btn-mini ${isBlocked ? 'btn-success-outline' : 'btn-danger'}" 
                      onclick="window.toggleBlockUser('${u.id}', ${!isBlocked})">
                ${isBlocked ? '차단 해제' : '차단'}
              </button>
              <button class="btn-mini btn-danger" onclick="window.adminDeleteUser('${u.id}')">
                삭제
              </button>
            ` : '<span style="color:var(--color-text-muted); font-size:11px;">변경 불가</span>'}
          </td>
        </tr>
      `;
    });
    els.adminMembersList.innerHTML = html;
  } catch (err) {
    console.error("Admin load members failed:", err);
  }
}

window.toggleBlockUser = async function(userId, blockState) {
  try {
    const res = await apiCall(`/api/admin/users/${userId}/block`, 'POST', { block: blockState });
    if (res.success) {
      alert(`계정이 ${blockState ? '정지' : '활성화'}되었습니다.`);
      await renderAdminMembers();
    }
  } catch (err) {
    alert("유저 차단 처리 실패");
  }
};

window.adminDeleteUser = async function(userId) {
  if (confirm(`정말 ID '${userId}' 회원 계정을 영구 삭제하시겠습니까?`)) {
    try {
      const res = await apiCall(`/api/admin/users/${userId}`, 'DELETE');
      if (res.success) {
        alert("계정이 삭제되었습니다.");
        await renderAdminMembers();
      }
    } catch (err) {
      alert("유저 삭제 실패");
    }
  }
};

async function renderAdminSongs() {
  await loadMusicList();
  let html = "";
  state.musicList.forEach(m => {
    html += `
      <tr>
        <td>
          <div style="display:flex; align-items:center; gap:10px;">
            <img src="${m.cover}" alt="Cover" style="width:36px; height:36px; border-radius:4px; object-fit:cover;">
            <span style="font-weight:700;">${escapeHtml(m.title)}</span>
          </div>
        </td>
        <td>${escapeHtml(m.artist)}</td>
        <td>
          <div class="hashtag-display-area">
            ${(m.tags || []).map(t => `<span class="tag-badge">#${escapeHtml(t)}</span>`).join('')}
          </div>
        </td>
        <td>❤️ ${m.likes}</td>
        <td class="admin-actions">
          <button class="btn-mini" onclick="window.adminEditSongPrompt('${m.id}')">수정</button>
          <button class="btn-mini btn-danger" onclick="window.adminDeleteSong('${m.id}')">삭제</button>
        </td>
      </tr>
    `;
  });
  els.adminSongsList.innerHTML = html;
}

async function handleAdminAddSong(e) {
  e.preventDefault();
  const title = els.adminSongTitle.value.trim();
  const artist = els.adminSongArtist.value.trim();
  let cover = els.adminSongCover.value.trim();
  const tagsString = els.adminSongTags.value.trim();
  
  if (!title || !artist) return;
  
  const tags = tagsString ? tagsString.split(',').map(t => t.trim()).filter(Boolean) : [];
  
  try {
    const res = await apiCall('/api/music', 'POST', {
      title,
      artist,
      cover,
      tags
    });
    if (res.success) {
      alert(`'${title}' 음원이 추가 등록되었습니다.`);
      els.adminAddSongForm.reset();
      await renderAdminSongs();
    }
  } catch (err) {
    alert("음원 등록 실패");
  }
}

window.adminEditSongPrompt = async function(songId) {
  const track = state.musicList.find(m => m.id === songId);
  if (!track) return;
  
  const newTitle = prompt("수정할 노래 제목을 입력하세요:", track.title);
  if (newTitle === null) return;
  const newArtist = prompt("수정할 아티스트명을 입력하세요:", track.artist);
  if (newArtist === null) return;
  
  if (newTitle.trim() && newArtist.trim()) {
    try {
      const res = await apiCall(`/api/music/${songId}`, 'PUT', {
        title: newTitle.trim(),
        artist: newArtist.trim()
      });
      if (res.success) {
        alert("정보가 수정되었습니다.");
        await renderAdminSongs();
      }
    } catch (err) {
      alert("정보 수정 실패");
    }
  }
};

window.adminDeleteSong = async function(songId) {
  if (confirm("정말 이 곡을 삭제하시겠습니까? 관련 댓글 정보도 함께 지워집니다.")) {
    try {
      const res = await apiCall(`/api/music/${songId}`, 'DELETE');
      if (res.success) {
        alert("삭제되었습니다.");
        await renderAdminSongs();
      }
    } catch (err) {
      alert("삭제 실패");
    }
  }
};

async function renderAdminComments() {
  try {
    const commentsList = await apiCall('/api/admin/comments');
    let html = "";
    commentsList.forEach(c => {
      const music = state.musicList.find(m => m.id === c.musicId);
      const musicTitle = music ? music.title : `알 수 없는 곡 (ID: ${c.musicId})`;
      const isReply = !!c.parentId;
      
      html += `
        <tr>
          <td><span style="font-size:11px; color:var(--color-primary);">${isReply ? '└─' : ''} ${escapeHtml(musicTitle)}</span></td>
          <td><strong>${escapeHtml(c.username)}</strong> (${escapeHtml(c.userId)})</td>
          <td style="max-width:250px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${escapeHtml(c.content)}">
            ${escapeHtml(c.content)}
          </td>
          <td style="font-size:11px; color:var(--color-text-muted);">${formatDate(c.timestamp)}</td>
          <td>
            <button class="btn-mini btn-danger" onclick="window.adminDeleteComment('${c.id}')">삭제</button>
          </td>
        </tr>
      `;
    });
    els.adminCommentsList.innerHTML = html || `<tr><td colspan="5" class="empty-state">시스템에 등록된 댓글이 없습니다.</td></tr>`;
  } catch (err) {
    console.error("Admin load comments failed:", err);
  }
}

window.adminDeleteComment = async function(commentId) {
  if (confirm("댓글을 정말 삭제하시겠습니까? (연결된 대댓글 포함)")) {
    try {
      const res = await apiCall(`/api/comments/${commentId}`, 'DELETE');
      if (res.success) {
        alert("삭제되었습니다.");
        await renderAdminComments();
      }
    } catch (err) {
      alert("댓글 삭제 실패");
    }
  }
};

/* persistent BOTTOM AUDIO PLAYER CONTROLLER */
function initAudioPlayer() {
  els.playerPlayPause.addEventListener('click', togglePlayback);
  els.playerPrev.addEventListener('click', playPreviousTrack);
  els.playerNext.addEventListener('click', playNextTrack);
  
  els.audio.addEventListener('timeupdate', updatePlaybackTimeline);
  els.audio.addEventListener('loadedmetadata', () => {
    els.playerTotalTime.innerText = formatDuration(els.audio.duration);
  });
  
  els.audio.addEventListener('ended', playNextTrack);
  
  els.playerProgressTrack.addEventListener('click', (e) => {
    if (!els.audio.duration) return;
    const rect = els.playerProgressTrack.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    els.audio.currentTime = percent * els.audio.duration;
  });
  
  els.playerVolumeTrack.addEventListener('click', (e) => {
    const rect = els.playerVolumeTrack.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    els.audio.volume = percent;
    els.playerVolumeFill.style.width = `${percent * 100}%`;
  });
  
  let isDraggingVolume = false;
  els.playerVolumeTrack.addEventListener('mousedown', () => isDraggingVolume = true);
  window.addEventListener('mouseup', () => isDraggingVolume = false);
  window.addEventListener('mousemove', (e) => {
    if (!isDraggingVolume) return;
    const rect = els.playerVolumeTrack.getBoundingClientRect();
    const percent = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    els.audio.volume = percent;
    els.playerVolumeFill.style.width = `${percent * 100}%`;
  });
}

function playTrack(index) {
  if (index < 0 || index >= state.musicList.length) return;
  state.currentTrackIndex = index;
  const track = state.musicList[index];
  
  els.audio.src = track.audioUrl;
  els.audio.play()
    .then(() => {
      state.isPlaying = true;
      updatePlayerUI(track);
    })
    .catch(err => {
      console.warn("Audio play error, playing client-side visually:", err);
      state.isPlaying = true;
      updatePlayerUI(track);
    });
}

function togglePlayback() {
  if (state.currentTrackIndex === -1 && state.musicList.length > 0) {
    playTrack(0);
    return;
  }
  
  if (state.isPlaying) {
    els.audio.pause();
    state.isPlaying = false;
    els.playerPlayIcon.style.display = 'block';
    els.playerPauseIcon.style.display = 'none';
    els.playerEq.classList.remove('playing');
  } else {
    els.audio.play()
      .then(() => {
        state.isPlaying = true;
        els.playerPlayIcon.style.display = 'none';
        els.playerPauseIcon.style.display = 'block';
        els.playerEq.classList.add('playing');
      })
      .catch(err => {
        console.warn("Audio play blocked, toggling visually:", err);
        state.isPlaying = true;
        els.playerPlayIcon.style.display = 'none';
        els.playerPauseIcon.style.display = 'block';
        els.playerEq.classList.add('playing');
      });
  }
}

function playPreviousTrack() {
  if (state.musicList.length === 0) return;
  let prevIdx = state.currentTrackIndex - 1;
  if (prevIdx < 0) prevIdx = state.musicList.length - 1;
  playTrack(prevIdx);
}

function playNextTrack() {
  if (state.musicList.length === 0) return;
  let nextIdx = state.currentTrackIndex + 1;
  if (nextIdx >= state.musicList.length) nextIdx = 0;
  playTrack(nextIdx);
}

function updatePlayerUI(track) {
  els.playerCover.src = track.cover;
  els.playerTitle.innerText = track.title;
  els.playerArtist.innerText = track.artist;
  
  els.playerPlayIcon.style.display = 'none';
  els.playerPauseIcon.style.display = 'block';
  els.playerEq.classList.add('playing');
}

function updatePlaybackTimeline() {
  if (!els.audio.duration) return;
  
  const current = els.audio.currentTime;
  const duration = els.audio.duration;
  const percent = (current / duration) * 100;
  
  els.playerProgressFill.style.width = `${percent}%`;
  els.playerCurrentTime.innerText = formatDuration(current);
}

/* HELPER FORMATTERS */
function escapeHtml(str) {
  if (!str) return '';
  return str.toString()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatDate(isoStr) {
  if (!isoStr) return "";
  const d = new Date(isoStr);
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
}

function formatDuration(sec) {
  if (isNaN(sec)) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

// Kick off
document.addEventListener('DOMContentLoaded', initApp);
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  initApp();
}
