from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Game, Stat
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    games_stats = (
        db.session.query(
            Game.name,
            Game.platform,
            func.count(func.distinct(Stat.user_id)).label('player_count'),
            func.sum(Stat.playtime).label('total_playtime')
        )
        .join(Stat, Game.id == Stat.game_id)
        .group_by(Game.id)
        .order_by(func.sum(Stat.playtime).desc())
        .all()
    )
    return render_template('home.html', games_stats=games_stats, background_video_url="https://cdn.coverr.co/videos/coverr-sci-fi-dome-1234/1080p.mp4")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html', background_video_url="https://cdn.coverr.co/videos/coverr-abstract-lights-5678/1080p.mp4")

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists.')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.')
            return redirect(url_for('main.login'))
    return render_template('register.html', background_video_url="https://cdn.coverr.co/videos/coverr-abstract-lights-5678/1080p.mp4")

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    stats = (
        db.session.query(
            Game.name,
            Game.platform,
            Stat.playtime,
            Stat.remarks
        )
        .join(Game, Game.id == Stat.game_id)
        .filter(Stat.user_id == current_user.id)
        .all()
    )
    return render_template('dashboard.html', stats=stats, background_video_url="https://cdn.coverr.co/videos/coverr-futuristic-tunnel-7464/1080p.mp4")

@bp.route('/add_stats', methods=['GET', 'POST'])
@login_required
def add_stats():
    if request.method == 'POST':
        game_title = request.form['game_title'].strip()
        platform = request.form['platform'].strip().lower()
        playtime = float(request.form['playtime'])
        remarks = request.form.get('remarks', '').strip()

        if platform not in ['pc', 'mobile', 'console']:
            flash('Invalid platform selected.', 'danger')
            return redirect(url_for('main.add_stats'))

        game = Game.query.filter_by(name=game_title, platform=platform).first()
        if not game:
            game = Game(name=game_title, platform=platform)
            db.session.add(game)
            db.session.commit()

        stat = Stat.query.filter_by(user_id=current_user.id, game_id=game.id).first()
        if stat:
            stat.playtime += playtime
            if remarks:
                stat.remarks = remarks
        else:
            stat = Stat(user_id=current_user.id, game_id=game.id, playtime=playtime, remarks=remarks if remarks else None)
            db.session.add(stat)

        db.session.commit()
        flash('Stats updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_stats.html', background_video_url="https://cdn.coverr.co/videos/coverr-cyberpunk-street-1234/1080p.mp4")

@bp.route('/leaderboard')
@login_required
def leaderboard():
    def get_leaders(platform):
        return db.session.query(
            User.username.label('Username'),
            func.sum(Stat.playtime).label('total_playtime')
        ).join(Stat, User.id == Stat.user_id)\
        .join(Game, Game.id == Stat.game_id)\
        .filter(Game.platform == platform)\
        .group_by(User.id)\
        .order_by(func.sum(Stat.playtime).desc())\
        .limit(10).all()

    pc_leaders = get_leaders('pc')
    mobile_leaders = get_leaders('mobile')
    console_leaders = get_leaders('console')

    return render_template('leaderboard.html', pc_leaders=pc_leaders, mobile_leaders=mobile_leaders, console_leaders=console_leaders, background_video_url="https://cdn.coverr.co/videos/coverr-hologram-street-9876/1080p.mp4")

@bp.route('/library')
@login_required
def library():
    games = Game.query.all()
    return render_template('library.html', games=games, background_video_url="https://cdn.coverr.co/videos/coverr-virtual-arcade-1357/1080p.mp4")

@bp.route('/developer')
def developer():
    return render_template('developer.html', background_video_url="https://cdn.coverr.co/videos/coverr-hacker-terminal-9999/1080p.mp4")
