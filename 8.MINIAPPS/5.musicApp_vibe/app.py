# -*- coding: utf-8 -*-
# app.py - MUSICAPP Flask Backend Server

from flask import Flask, jsonify, request, render_template, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "musicapp_super_secret_key_1234!"

DB_FILE = "db.json"

DEFAULT_USERS = [
    { "id": "user1", "username": "VibeSeeker", "password": "123", "avatar": "avatar1", "bio": "음악에 살고 음악에 죽는 리스너입니다. 🎧", "status": "active", "role": "user" },
    { "id": "user2", "username": "MelodyQueen", "password": "123", "avatar": "avatar2", "bio": "팝송과 인디음악을 주로 들어요. 🎵", "status": "active", "role": "user" },
    { "id": "user3", "username": "SynthWave_Fan", "password": "123", "avatar": "avatar3", "bio": "80년대 레트로 신스웨이브 매니아 ⚡", "status": "active", "role": "user" },
    { "id": "emp1", "username": "관리자1", "password": "1234", "avatar": "admin", "bio": "MUSICAPP 공식 시스템 관리자", "status": "active", "role": "admin" }
]

DEFAULT_MUSIC = [
    {
        "id": "m1",
        "title": "Midnight City Groove",
        "artist": "Neon Skyline",
        "album": "Synth Horizons",
        "cover": "https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80",
        "likes": 124,
        "tags": ["Synthwave", "Chill", "Retro", "Focus"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "duration": "6:12"
    },
    {
        "id": "m2",
        "title": "Summer Breeze",
        "artist": "Chilled Waves",
        "album": "Coastal Drive",
        "cover": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=400&q=80",
        "likes": 98,
        "tags": ["Chill", "Pop", "Summer", "K-Pop"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "duration": "7:05"
    },
    {
        "id": "m3",
        "title": "Neon Hearts",
        "artist": "Retro Love",
        "album": "Lovesick Cyberpunk",
        "cover": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400&q=80",
        "likes": 87,
        "tags": ["Synthwave", "Dance", "Retro"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "duration": "5:44"
    },
    {
        "id": "m4",
        "title": "Deep Coffee Study",
        "artist": "Lo-Fi Beats",
        "album": "Rainy Day Cafe",
        "cover": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=400&q=80",
        "likes": 76,
        "tags": ["Lo-Fi", "Chill", "Focus", "Study"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "duration": "5:02"
    },
    {
        "id": "m5",
        "title": "Cyberpunk Runner",
        "artist": "Laser Knight",
        "album": "Overdrive Phase 2",
        "cover": "https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=400&q=80",
        "likes": 72,
        "tags": ["Workout", "Dance", "Synthwave", "Exciting"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
        "duration": "6:03"
    },
    {
        "id": "m6",
        "title": "Spring Blossoms",
        "artist": "Min-ji Park",
        "album": "Acoustic Seasons",
        "cover": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&q=80",
        "likes": 65,
        "tags": ["K-Pop", "Acoustic", "Spring", "Chill"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3",
        "duration": "5:38"
    },
    {
        "id": "m7",
        "title": "Electric Horizon",
        "artist": "Future Bass",
        "album": "Vivid Dreams",
        "cover": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400&q=80",
        "likes": 58,
        "tags": ["Dance", "Workout", "Exciting"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3",
        "duration": "5:07"
    },
    {
        "id": "m8",
        "title": "Quiet Library",
        "artist": "Study Companion",
        "album": "White Noise Essentials",
        "cover": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&q=80",
        "likes": 49,
        "tags": ["Study", "Focus", "Chill"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        "duration": "5:18"
    },
    {
        "id": "m9",
        "title": "Late Night Jazz Bar",
        "artist": "The Blue Notes Trio",
        "album": "Standard Moods",
        "cover": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=400&q=80",
        "likes": 42,
        "tags": ["Jazz", "Chill", "Classic"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
        "duration": "5:42"
    },
    {
        "id": "m10",
        "title": "Run Fast",
        "artist": "Beat Drifter",
        "album": "Cardio Hits",
        "cover": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400&q=80",
        "likes": 38,
        "tags": ["Workout", "Exciting", "Dance"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
        "duration": "5:23"
    },
    {
        "id": "m11",
        "title": "Lo-Fi Ocean Waves",
        "artist": "Sandy Beaches",
        "album": "Coastal Lo-Fi",
        "cover": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&q=80",
        "likes": 31,
        "tags": ["Lo-Fi", "Chill", "Summer"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-11.mp3",
        "duration": "6:08"
    },
    {
        "id": "m12",
        "title": "Supernova Disco",
        "artist": "Galaxy Groovers",
        "album": "Disco Nebula",
        "cover": "https://images.unsplash.com/photo-1483412033650-1015ddeb83d1?w=400&q=80",
        "likes": 27,
        "tags": ["Dance", "Exciting", "Retro"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3",
        "duration": "5:58"
    },
    {
        "id": "m13",
        "title": "Rainy Afternoon Melody",
        "artist": "Piano Oasis",
        "album": "Cozy Piano Keys",
        "cover": "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80",
        "likes": 19,
        "tags": ["Acoustic", "Chill", "Study"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-13.mp3",
        "duration": "5:10"
    },
    {
        "id": "m14",
        "title": "K-Pop Sparkle",
        "artist": "Star Project",
        "album": "Rising Star Single",
        "cover": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&q=80",
        "likes": 15,
        "tags": ["K-Pop", "Dance", "Exciting"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-14.mp3",
        "duration": "5:17"
    },
    {
        "id": "m15",
        "title": "Focus Ambient Wave",
        "artist": "Zen Mind",
        "album": "Calm Waves",
        "cover": "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=400&q=80",
        "likes": 8,
        "tags": ["Focus", "Study", "Chill"],
        "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3",
        "duration": "6:33"
    }
]

DEFAULT_COMMENTS = [
    {
        "id": "c_1",
        "musicId": "m1",
        "userId": "user2",
        "username": "MelodyQueen",
        "avatar": "avatar2",
        "content": "이 곡 신스 소리가 너무 환상적이에요! 매일 퇴근할 때 듣고 있습니다. 😍",
        "timestamp": "2026-05-20T18:30:00Z",
        "likes": ["user1", "user3"]
    },
    {
        "id": "c_2",
        "musicId": "m1",
        "userId": "user1",
        "username": "VibeSeeker",
        "avatar": "avatar1",
        "content": "맞아요, 80년대 감성 지대루네요. 특히 리듬이 쫀득합니다.",
        "parentId": "c_1",
        "timestamp": "2026-05-20T19:02:00Z",
        "likes": ["user2"]
    },
    {
        "id": "c_3",
        "musicId": "m4",
        "userId": "user3",
        "username": "SynthWave_Fan",
        "avatar": "avatar3",
        "content": "시험 공부할 때 백그라운드로 틀어놓기 최고입니다. 집중 잘 됨!",
        "timestamp": "2026-05-21T01:10:00Z",
        "likes": ["user2"]
    },
    {
        "id": "c_4",
        "musicId": "m2",
        "userId": "user1",
        "username": "VibeSeeker",
        "avatar": "avatar1",
        "content": "여름 드라이브 갈 때 완전 필수곡! 청량감 미쳤어요 🌊",
        "timestamp": "2026-05-21T05:20:00Z",
        "likes": []
    }
]

DEFAULT_NOTIFICATIONS = [
    {
        "id": "n_1",
        "recipientId": "user2",
        "senderId": "user1",
        "senderName": "VibeSeeker",
        "type": "reply",
        "musicId": "m1",
        "musicTitle": "Midnight City Groove",
        "commentId": "c_1",
        "content": "맞아요, 80년대 감성 지대루네요. 특히 리듬이 쫀득합니다.",
        "timestamp": "2026-05-20T19:02:00Z",
        "read": False
    },
    {
        "id": "n_2",
        "recipientId": "user2",
        "senderId": "user3",
        "senderName": "SynthWave_Fan",
        "type": "like",
        "musicId": "m1",
        "musicTitle": "Midnight City Groove",
        "commentId": "c_1",
        "content": "회원님의 댓글을 좋아합니다.",
        "timestamp": "2026-05-20T21:40:00Z",
        "read": False
    }
]

# Load DB or Initialize
def load_db():
    if not os.path.exists(DB_FILE):
        db = {
            "users": DEFAULT_USERS,
            "music": DEFAULT_MUSIC,
            "comments": DEFAULT_COMMENTS,
            "notifications": DEFAULT_NOTIFICATIONS,
            "likes": {} # { userId: [musicIds...] }
        }
        save_db(db)
        return db
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading database, resetting...:", e)
        db = {
            "users": DEFAULT_USERS,
            "music": DEFAULT_MUSIC,
            "comments": DEFAULT_COMMENTS,
            "notifications": DEFAULT_NOTIFICATIONS,
            "likes": {}
        }
        save_db(db)
        return db

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home_index():
    return render_template('index.html')

# AUTH APIs
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json or {}
    uid = data.get("id", "").strip()
    pw = data.get("password", "").strip()
    
    db = load_db()
    
    # Auto admin detection for ID emp[0-9]+ with password 1234
    is_admin_format = uid.lower().startswith("emp") and uid[3:].isdigit()
    
    user = next((u for u in db["users"] if u["id"].lower() == uid.lower()), None)
    
    if is_admin_format:
        if pw == "1234":
            if not user:
                # Add to DB dynamically
                user = {
                    "id": uid.lower(),
                    "username": f"관리자({uid})",
                    "password": "1234",
                    "avatar": "admin",
                    "bio": "MUSICAPP 시스템 관리자",
                    "status": "active",
                    "role": "admin"
                }
                db["users"].append(user)
                save_db(db)
        else:
            return jsonify({ "success": False, "message": "관리자 비밀번호는 1234 입니다." }), 400
            
    if not user:
        return jsonify({ "success": False, "message": "가입되지 않은 아이디입니다." }), 404
        
    if user["password"] != pw:
        return jsonify({ "success": False, "message": "비밀번호가 올바르지 않습니다." }), 400
        
    if user.get("status") == "blocked":
        return jsonify({ "success": False, "message": "정지된 계정입니다. 관리자에게 문의하세요." }), 403
        
    return jsonify({ "success": True, "user": user })

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.json or {}
    uid = data.get("id", "").strip()
    username = data.get("username", "").strip()
    pw = data.get("password", "").strip()
    
    if not uid or not username or not pw:
        return jsonify({ "success": False, "message": "모든 필드를 채워주세요." }), 400
        
    if uid.lower().startswith("emp"):
        return jsonify({ "success": False, "message": "emp로 시작하는 아이디는 관리자 전용입니다." }), 400
        
    db = load_db()
    if any(u["id"].lower() == uid.lower() for u in db["users"]):
        return jsonify({ "success": False, "message": "이미 존재하는 아이디입니다." }), 400
        
    new_user = {
        "id": uid,
        "username": username,
        "password": pw,
        "avatar": "avatar1",
        "bio": "음악을 사랑합니다.",
        "status": "active",
        "role": "user"
    }
    db["users"].append(new_user)
    save_db(db)
    return jsonify({ "success": True, "message": "회원가입에 성공했습니다." })

# MUSIC LIST APIs
@app.route('/api/music', methods=['GET'])
def api_get_music():
    db = load_db()
    return jsonify(db["music"])

@app.route('/api/music', methods=['POST'])
def api_add_music():
    # Admin only
    data = request.json or {}
    db = load_db()
    
    # Generate unique ID
    new_id = "m" + str(len(db["music"]) + 1) + "_" + os.urandom(2).hex()
    
    new_song = {
        "id": new_id,
        "title": data.get("title"),
        "artist": data.get("artist"),
        "album": data.get("album", "Single Release"),
        "cover": data.get("cover") or f"https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80",
        "likes": 0,
        "tags": data.get("tags", []),
        "audioUrl": data.get("audioUrl") or "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "duration": data.get("duration", "5:00")
    }
    db["music"].append(new_song)
    save_db(db)
    return jsonify({ "success": True, "music": new_song })

@app.route('/api/music/<music_id>', methods=['PUT'])
def api_edit_music(music_id):
    data = request.json or {}
    db = load_db()
    
    song = next((m for m in db["music"] if m["id"] == music_id), None)
    if not song:
        return jsonify({ "success": False, "message": "음원을 찾을 수 없습니다." }), 404
        
    song["title"] = data.get("title", song["title"])
    song["artist"] = data.get("artist", song["artist"])
    if "tags" in data:
        song["tags"] = data["tags"]
        
    save_db(db)
    return jsonify({ "success": True, "music": song })

@app.route('/api/music/<music_id>', methods=['DELETE'])
def api_delete_music(music_id):
    db = load_db()
    db["music"] = [m for m in db["music"] if m["id"] != music_id]
    db["comments"] = [c for c in db["comments"] if c["musicId"] != music_id]
    save_db(db)
    return jsonify({ "success": True })

# LIKE MUSIC
@app.route('/api/music/<music_id>/like', methods=['POST'])
def api_like_music(music_id):
    data = request.json or {}
    user_id = data.get("userId")
    if not user_id:
        return jsonify({ "success": False, "message": "로그인이 필요한 서비스입니다." }), 401
        
    db = load_db()
    likes = db.get("likes", {})
    if user_id not in likes:
        likes[user_id] = []
        
    song = next((m for m in db["music"] if m["id"] == music_id), None)
    if not song:
        return jsonify({ "success": False, "message": "곡을 찾을 수 없습니다." }), 404
        
    if music_id in likes[user_id]:
        # Unlike
        likes[user_id].remove(music_id)
        song["likes"] = max(0, song["likes"] - 1)
        action = "unlike"
    else:
        # Like
        likes[user_id].append(music_id)
        song["likes"] += 1
        action = "like"
        
    db["likes"] = likes
    save_db(db)
    return jsonify({ "success": True, "likes": song["likes"], "action": action })

# HASHTAG ADD
@app.route('/api/music/<music_id>/tag', methods=['POST'])
def api_add_tag(music_id):
    data = request.json or {}
    new_tag = data.get("tag", "").strip().replace("#", "")
    if not new_tag:
        return jsonify({ "success": False, "message": "올바른 태그를 입력하세요." }), 400
        
    db = load_db()
    song = next((m for m in db["music"] if m["id"] == music_id), None)
    if not song:
        return jsonify({ "success": False, "message": "음원을 찾을 수 없습니다." }), 404
        
    if "tags" not in song:
        song["tags"] = []
        
    if new_tag in song["tags"]:
        return jsonify({ "success": False, "message": "이미 등록된 태그입니다." }), 400
        
    song["tags"].append(new_tag)
    save_db(db)
    return jsonify({ "success": True, "tags": song["tags"] })

# COMMENTS APIs
@app.route('/api/comments/<music_id>', methods=['GET'])
def api_get_comments(music_id):
    db = load_db()
    song_comments = [c for c in db["comments"] if c["musicId"] == music_id]
    return jsonify(song_comments)

@app.route('/api/comments', methods=['POST'])
def api_add_comment():
    data = request.json or {}
    music_id = data.get("musicId")
    user_id = data.get("userId")
    username = data.get("username")
    avatar = data.get("avatar")
    content = data.get("content", "").strip()
    parent_id = data.get("parentId") # optional (for nested comments)
    
    if not music_id or not user_id or not content:
        return jsonify({ "success": False, "message": "필수 입력 값이 유실되었습니다." }), 400
        
    db = load_db()
    comment_id = "c_" + str(int(datetime.now().timestamp() * 1000))
    
    new_comment = {
        "id": comment_id,
        "musicId": music_id,
        "userId": user_id,
        "username": username,
        "avatar": avatar,
        "content": content,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "likes": []
    }
    
    if parent_id:
        new_comment["parentId"] = parent_id
        
        # Trigger notification to parent comment owner
        parent_comment = next((c for c in db["comments"] if c["id"] == parent_id), None)
        if parent_comment and parent_comment["userId"] != user_id:
            song = next((m for m in db["music"] if m["id"] == music_id), None)
            notif = {
                "id": "n_" + str(int(datetime.now().timestamp() * 1000)),
                "recipientId": parent_comment["userId"],
                "senderId": user_id,
                "senderName": username,
                "type": "reply",
                "musicId": music_id,
                "musicTitle": song["title"] if song else "음악",
                "commentId": parent_id,
                "content": content[:30],
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "read": False
            }
            db["notifications"].append(notif)
            
    db["comments"].append(new_comment)
    save_db(db)
    return jsonify({ "success": True, "comment": new_comment })

@app.route('/api/comments/<comment_id>/like', methods=['POST'])
def api_like_comment(comment_id):
    data = request.json or {}
    user_id = data.get("userId")
    if not user_id:
        return jsonify({ "success": False, "message": "로그인이 필요합니다." }), 401
        
    db = load_db()
    comment = next((c for c in db["comments"] if c["id"] == comment_id), None)
    if not comment:
        return jsonify({ "success": False, "message": "댓글을 찾을 수 없습니다." }), 404
        
    if "likes" not in comment:
        comment["likes"] = []
        
    if user_id in comment["likes"]:
        comment["likes"].remove(user_id)
        action = "unlike"
    else:
        comment["likes"].append(user_id)
        action = "like"
        
        # Notify comment author
        if comment["userId"] != user_id:
            song = next((m for m in db["music"] if m["id"] == comment["musicId"]), None)
            notif = {
                "id": "n_" + str(int(datetime.now().timestamp() * 1000)),
                "recipientId": comment["userId"],
                "senderId": user_id,
                "senderName": data.get("username", "누군가"),
                "type": "like",
                "musicId": comment["musicId"],
                "musicTitle": song["title"] if song else "음악",
                "commentId": comment_id,
                "content": "회원님의 댓글을 좋아합니다.",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "read": False
            }
            db["notifications"].append(notif)
            
    save_db(db)
    return jsonify({ "success": True, "likesCount": len(comment["likes"]), "action": action })

@app.route('/api/comments/<comment_id>', methods=['DELETE'])
def api_delete_comment(comment_id):
    db = load_db()
    # Delete the comment and any replies
    db["comments"] = [c for c in db["comments"] if c["id"] != comment_id and c.get("parentId") != comment_id]
    save_db(db)
    return jsonify({ "success": True })

# NOTIFICATIONS APIs
@app.route('/api/notifications/<user_id>', methods=['GET'])
def api_get_notifications(user_id):
    db = load_db()
    user_notifs = [n for n in db["notifications"] if n["recipientId"] == user_id]
    return jsonify(user_notifs)

@app.route('/api/notifications/<notif_id>/read', methods=['POST'])
def api_read_notification(notif_id):
    db = load_db()
    notif = next((n for n in db["notifications"] if n["id"] == notif_id), None)
    if notif:
        notif["read"] = True
        save_db(db)
    return jsonify({ "success": True })

@app.route('/api/notifications/<user_id>', methods=['DELETE'])
def api_clear_notifications(user_id):
    db = load_db()
    db["notifications"] = [n for n in db["notifications"] if n["recipientId"] != user_id]
    save_db(db)
    return jsonify({ "success": True })

# PROFILE UPDATE
@app.route('/api/profile', methods=['POST'])
def api_update_profile():
    data = request.json or {}
    user_id = data.get("userId")
    new_username = data.get("username", "").strip()
    new_avatar = data.get("avatar")
    
    if not user_id or not new_username:
        return jsonify({ "success": False, "message": "잘못된 요청 정보입니다." }), 400
        
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        return jsonify({ "success": False, "message": "사용자를 찾을 수 없습니다." }), 404
        
    user["username"] = new_username
    if new_avatar:
        user["avatar"] = new_avatar
        
    # Update comments username & avatar cache
    for c in db["comments"]:
        if c["userId"] == user_id:
            c["username"] = new_username
            if new_avatar:
                c["avatar"] = new_avatar
                
    save_db(db)
    return jsonify({ "success": True, "user": user })

@app.route('/api/profile/comments/<user_id>', methods=['GET'])
def api_get_user_comments(user_id):
    db = load_db()
    user_comments = [c for c in db["comments"] if c["userId"] == user_id]
    return jsonify(user_comments)

# ADMIN MANAGEMENT APIs
@app.route('/api/admin/users', methods=['GET'])
def api_admin_get_users():
    db = load_db()
    return jsonify(db["users"])

@app.route('/api/admin/users/<user_id>/block', methods=['POST'])
def api_admin_block_user(user_id):
    data = request.json or {}
    block_state = data.get("block", False)
    
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        return jsonify({ "success": False, "message": "사용자를 찾을 수 없습니다." }), 404
        
    if user.get("role") == "admin":
        return jsonify({ "success": False, "message": "관리자는 차단할 수 없습니다." }), 400
        
    user["status"] = "blocked" if block_state else "active"
    save_db(db)
    return jsonify({ "success": True, "status": user["status"] })

@app.route('/api/admin/users/<user_id>', methods=['DELETE'])
def api_admin_delete_user(user_id):
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        return jsonify({ "success": False, "message": "사용자를 찾을 수 없습니다." }), 404
        
    if user.get("role") == "admin":
        return jsonify({ "success": False, "message": "관리자는 삭제할 수 없습니다." }), 400
        
    db["users"] = [u for u in db["users"] if u["id"] != user_id]
    # Clean likes
    if user_id in db.get("likes", {}):
        del db["likes"][user_id]
        
    save_db(db)
    return jsonify({ "success": True })

@app.route('/api/admin/comments', methods=['GET'])
def api_admin_get_all_comments():
    db = load_db()
    return jsonify(db["comments"])

if __name__ == "__main__":
    load_db() # Preload database on start
    app.run(host="0.0.0.0", port=5000, debug=True)
