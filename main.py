from flask import Flask, render_template, request, redirect, url_for, flash
from editor.ai import auto_edit_video, recognize_objects, transcribe_audio, analyze_sentiment, optimize_content
from editor.editor import upload_video, save_project, export_video
from editor.utils import init_app_config
from config.settings import APP_CONFIG

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(APP_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' in request.files:
        video_file = request.files['video']
        upload_video(video_file)
        flash('Video uploaded successfully!', 'VideoUploadSuccess')
        return redirect(url_for('editor'))
    else:
        flash('An error occurred while uploading the video.', 'ErrorOccurred')
        return redirect(url_for('index'))

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/edit/auto', methods=['POST'])
def auto_edit():
    try:
        style = request.form.get('style')
        video_path = request.form.get('video_path')
        edited_video_path = auto_edit_video(video_path, style)
        flash('Auto-editing complete!', 'EditComplete')
        return redirect(url_for('editor', video_path=edited_video_path))
    except Exception as e:
        flash(str(e), 'ErrorOccurred')
        return redirect(url_for('editor'))

@app.route('/edit/save', methods=['POST'])
def save():
    try:
        project_data = request.form.get('project_data')
        save_project(project_data)
        flash('Project saved successfully!', 'EditComplete')
        return redirect(url_for('editor'))
    except Exception as e:
        flash(str(e), 'ErrorOccurred')
        return redirect(url_for('editor'))

@app.route('/edit/export', methods=['POST'])
def export():
    try:
        project_id = request.form.get('project_id')
        export_video(project_id)
        flash('Video exported successfully!', 'EditComplete')
        return redirect(url_for('editor'))
    except Exception as e:
        flash(str(e), 'ErrorOccurred')
        return redirect(url_for('editor'))

if __name__ == '__main__':
    init_app_config(app)
    app.run(debug=app.config['DEBUG'])