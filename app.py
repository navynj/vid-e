from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import split

app = Flask(__name__)
UPLOAD_FOLDER = '/Users/gimjin-a/Desktop/flask_upload/static/uploads/'

#업로드 HTML 렌더링
@app.route('/')
def render_file():
   return render_template('play.html')

#파일 업로드 처리
@app.route('/play', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      tdb = request.form['topdb']
      sr, non_mute_intervals, tdb = split.get_non_mute(tdb)
      fname = str(tdb)+ "_split.wav"
      split.remove_silence(sr, non_mute_intervals)
      return render_template('play.html', tdb = tdb, source = "uploads/" + fname)
      #output = tdb)

if __name__ == '__main__':
    #서버 실행
   app.run(debug = True)
