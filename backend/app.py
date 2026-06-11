from flask import Flask, send_from_directory, request, jsonify, session
from flask_cors import CORS
import sqlite3
import os
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'shu-blog-secret-key-2024'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
CORS(app, supports_credentials=True, origins=[
    'https://shuhunb515.github.io',
    'http://localhost:3000'
])


IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize DB tables and default data."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS learning (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, content TEXT, sort_order INTEGER DEFAULT 0, views INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now','localtime')))")
    conn.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, content TEXT, file_path TEXT, sort_order INTEGER DEFAULT 0, views INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now','localtime')))")

    # Default admin user
    cur = conn.execute("SELECT COUNT(*) as cnt FROM users")
    if cur.fetchone()['cnt'] == 0:
        pwd_hash = hashlib.sha256('Hu200692?'.encode()).hexdigest()
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ('shuhu', pwd_hash))

    # Default learning data - load from static files
    cur = conn.execute("SELECT COUNT(*) as cnt FROM learning")
    if cur.fetchone()['cnt'] == 0:
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        learning_files = [
            ('learning_html_css.md', 'HTML & CSS', '大一上学期 - 网页设计与布局基础', 1),
            ('learning_js.md', 'JavaScript', '大一下学期 - 前端交互编程', 2),
            ('learning_python.md', 'Python', '大一下学期 - 编程语言与后端开发', 3),
            ('learning_vue.md', 'Vue 3', '大二上学期 - 渐进式前端框架', 4),
            ('learning_algorithm.md', 'Python 算法竞赛', '大二上学期至今 - 算法练习与竞赛准备', 5),
        ]
        for filename, title, desc, order in learning_files:
            filepath = os.path.join(static_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                conn.execute("INSERT INTO learning (title, description, content, sort_order) VALUES (?, ?, ?, ?)",
                    (title, desc, content, order))

    # Default projects
    cur = conn.execute("SELECT COUNT(*) as cnt FROM projects")
    if cur.fetchone()['cnt'] == 0:
        conn.execute("INSERT INTO projects (title, description, content, file_path, sort_order) VALUES (?, ?, ?, ?, ?)",
            ('Shu Blog', '个人博客系统',
             '## 技术栈\n\n- 前端：Vue 3 + Vite + Vue Router\n- 后端：Python Flask + SQLite\n- 特性：登录认证、CRUD 管理、浏览量统计、Canvas 动画\n\n## 功能亮点\n\n- 响应式设计，深色主题\n- 雨滴粒子动画 + 双重波浪特效\n- 底部小车动画效果\n- 管理员内容管理系统', '', 1))
        conn.execute("INSERT INTO projects (title, description, content, file_path, sort_order) VALUES (?, ?, ?, ?, ?)",
            ('打造独立操作系统内核', '从零开始构建不属于 Windows 也不属于 Linux 的独立操作系统内核。涵盖 Bare Bones 环境搭建、交叉编译器构建、汇编启动入口、C 语言内核主程序、VGA 显存输出。',
             '## 项目简介\n\n从零开始打造一个完全独立于现有系统的自定义操作系统内核，基于 x86 架构实现最底层硬件交互。', 'os-kernel.md', 2))
        conn.execute("INSERT INTO projects (title, description, content, file_path, sort_order) VALUES (?, ?, ?, ?, ?)",
            ('创建 Linux 发行版 (shu-linux)', '亲手从 LFS/BLFS 构建一个名为 shu-linux 的完整 Linux 发行版。',
             '## 项目简介\n\n从零构建专属 Linux 发行版 shu-linux，深入理解 Linux 系统的每一个组件。', 'linux-distro.md', 3))
        conn.execute("INSERT INTO projects (title, description, content, file_path, sort_order) VALUES (?, ?, ?, ?, ?)",
            ('安装 D-Bus 核心组件', '在 shu-linux 发行版上安装和配置 D-Bus 核心组件，解决 BLFS 构建过程中的依赖问题。',
             '## 项目简介\n\n在 shu-linux 上部署 D-Bus 消息总线系统，解决 BLFS 构建链中的各种编译与依赖问题。', 'dbus-components.md', 4))

    conn.commit()
    conn.close()


# ==================== Auth ====================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, pwd_hash)).fetchone()
    conn.close()
    if user:
        session['user'] = username
        return jsonify({'code': 200, 'message': '登录成功'})
    return jsonify({'code': 401, 'message': '用户名或密码错误'})

@app.route('/api/logout')
def logout():
    session.pop('user', None)
    return jsonify({'code': 200, 'message': '已登出'})

@app.route('/api/check-login')
def check_login():
    if session.get('user'):
        return jsonify({'code': 200, 'username': session['user']})
    return jsonify({'code': 401, 'message': '未登录'})

# ==================== Learning ====================

@app.route('/api/learning')
def get_learning_list():
    conn = get_db()
    rows = conn.execute("SELECT id, title, description, sort_order, views, created_at FROM learning ORDER BY sort_order").fetchall()
    conn.close()
    return jsonify({'code': 200, 'data': [dict(r) for r in rows]})

@app.route('/api/learning/<int:lid>')
def get_learning_detail(lid):
    conn = get_db()
    row = conn.execute("SELECT * FROM learning WHERE id=?", (lid,)).fetchone()
    if row:
        conn.execute("UPDATE learning SET views = views + 1 WHERE id=?", (lid,))
        conn.commit()
    conn.close()
    if row:
        return jsonify({'code': 200, 'data': dict(row)})
    return jsonify({'code': 404, 'message': '未找到'})

@app.route('/api/learning', methods=['POST'])
def add_learning():
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO learning (title, description, content, sort_order) VALUES (?, ?, ?, ?)",
        (data.get('title'), data.get('description'), data.get('content'), data.get('sort_order', 0)))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '添加成功'})

@app.route('/api/learning/<int:lid>', methods=['PUT'])
def update_learning(lid):
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    data = request.get_json()
    conn = get_db()
    conn.execute("UPDATE learning SET title=?, description=?, content=?, sort_order=? WHERE id=?",
        (data.get('title'), data.get('description'), data.get('content'), data.get('sort_order', 0), lid))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功'})

@app.route('/api/learning/<int:lid>', methods=['DELETE'])
def delete_learning(lid):
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    conn = get_db()
    conn.execute("DELETE FROM learning WHERE id=?", (lid,))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功'})

# ==================== Projects ====================

@app.route('/api/projects')
def get_projects():
    conn = get_db()
    rows = conn.execute("SELECT id, title, description, file_path, sort_order, views, created_at FROM projects ORDER BY sort_order").fetchall()
    conn.close()
    return jsonify({'code': 200, 'data': [dict(r) for r in rows]})

@app.route('/api/projects/<int:pid>')
def get_project_detail(pid):
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    if row:
        conn.execute("UPDATE projects SET views = views + 1 WHERE id=?", (pid,))
        conn.commit()
    conn.close()
    if row:
        return jsonify({'code': 200, 'data': dict(row)})
    return jsonify({'code': 404, 'message': '未找到'})

@app.route('/api/projects', methods=['POST'])
def add_project():
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    data = request.get_json()
    conn = get_db()
    conn.execute("INSERT INTO projects (title, description, content, file_path, sort_order) VALUES (?, ?, ?, ?, ?)",
        (data.get('title'), data.get('description'), data.get('content'), data.get('file_path', ''), data.get('sort_order', 0)))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '添加成功'})

@app.route('/api/projects/<int:pid>', methods=['PUT'])
def update_project(pid):
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    data = request.get_json()
    conn = get_db()
    conn.execute("UPDATE projects SET title=?, description=?, content=?, file_path=?, sort_order=? WHERE id=?",
        (data.get('title'), data.get('description'), data.get('content'), data.get('file_path', ''), data.get('sort_order', 0), pid))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '更新成功'})

@app.route('/api/projects/<int:pid>', methods=['DELETE'])
def delete_project(pid):
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    conn = get_db()
    conn.execute("DELETE FROM projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功'})

@app.route('/api/projects/md/<filename>')
def serve_markdown(filename):
    import os
    safe_name = os.path.basename(filename)
    md_path = os.path.join(os.path.dirname(__file__), 'static', 'projects', safe_name)
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'code': 200, 'data': content})
    return jsonify({'code': 404, 'message': '文件未找到'})

# ==================== Stats ====================

@app.route('/api/stats')
def get_stats():
    if not session.get('user'):
        return jsonify({'code': 403, 'message': '请先登录'})
    conn = get_db()
    learning_rows = conn.execute("SELECT title, views FROM learning ORDER BY sort_order").fetchall()
    project_rows = conn.execute("SELECT title, views FROM projects ORDER BY sort_order").fetchall()
    conn.close()
    by_page = []
    total = 0
    for r in learning_rows:
        by_page.append({'page': r['title'], 'count': r['views']})
        total += r['views']
    for r in project_rows:
        by_page.append({'page': r['title'], 'count': r['views']})
        total += r['views']
    return jsonify({'code': 200, 'data': {'total': total, 'byPage': by_page}})

# ==================== Images ====================

@app.route('/api/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
