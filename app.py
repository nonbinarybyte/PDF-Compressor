
from flask import Flask, request, send_file
import subprocess
import os
from tempfile import NamedTemporaryFile

app = Flask(__name__)

@app.route('/')
def home():
    return open("templates/index.html").read()

@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files['pdf']
    input_temp = NamedTemporaryFile(delete=False, suffix='.pdf')
    output_temp = NamedTemporaryFile(delete=False, suffix='.pdf')

    file.save(input_temp.name)

    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE",
        "-dBATCH",
        "-sOutputFile=" + output_temp.name,
        input_temp.name
    ]

    subprocess.run(gs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return send_file(output_temp.name, download_name="compressed.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
