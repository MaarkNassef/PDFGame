from flask import Flask, request, redirect, render_template, url_for, send_file, flash
from datetime import datetime
import hashlib
from convert import convert_file
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "Powerful secret key"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash("Choose a file")
            return render_template('index.html')
        elif file.filename.split('.')[-1].lower() != 'pdf':
            flash("Choose a valid PDF file")
            return render_template('index.html')
        else:
            filename=hashlib.md5(str(datetime.now()).encode()).hexdigest()
            file.save(f'temp/upload/{filename}.pdf')
            return redirect(url_for('convert', filename=filename))
    return render_template('index.html')

@app.route('/convert/<string:filename>')
def convert(filename: str):
    new_file_path = convert_file(filename)
    try:
        os.remove(os.path.relpath(f'temp/upload/{filename}.pdf'))
    except:
        pass
    return render_template('convert.html', filepath=new_file_path)


@app.route('/download/<path:filepath>')
def download_file(filepath):
    try:
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return str(e)
    
@app.route('/remove/<path:filepath>')
def remove(filepath: str):
    try:
        os.remove(os.path.relpath(filepath))
    except:
        pass
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)