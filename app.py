from flask import Flask, request, redirect, render_template, url_for, send_file, flash
from datetime import datetime
import hashlib
from convert import convert
import io

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
            content = file.read()
            result = convert(content=content)
            new_filename = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()
            return send_file(
                io.BytesIO(result.tobytes()),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'{new_filename}.pdf'
            )
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)