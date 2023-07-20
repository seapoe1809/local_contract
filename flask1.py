
from flask import Flask, render_template, send_from_directory, session, request, redirect
from urllib.parse import quote, unquote
import webbrowser
import os, subprocess
import getpass
import qrcode


app = Flask(__name__)
app.secret_key = 'your_secret_key_power_to_decentralized'


# Configure static folder path
app.static_folder = 'static'


@app.route('/')
def home():
    if 'logged_in' in session:
        # User is logged in, redirect to the protected page
        return render_template('index.html')
    else:
        # User is not logged in, redirect to the login page
        return redirect('/login')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']

        # Check if the password is correct
        if password == 'power':
            # Password is correct, set the login status in the session
            session['logged_in'] = True
            return redirect('/')
        else:
            # Password is incorrect, show an error message
            error_message = ''
            return render_template('login.html', error_message=error_message)

    # Render the login page template
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the login status from the session
    session.pop('logged_in', None)
    return redirect('/login')

#making links for folder directory and files
@app.route('/folder')
def folder_index():
    if 'logged_in' not in session:
        return redirect('/login')

    folder_path = folderpath

    files = []
    files = os.listdir(folder_path)

    file_links = []

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        is_directory = os.path.isdir(file_path)

        if is_directory:
            file_links.append({'filename': filename, 'path': f'/folder/{filename}', 'is_folder': True})
        else:
            file_links.append({'filename': filename, 'path': f'/{filename}', 'is_folder': False})

    return render_template('folder_index.html', files=file_links)

#serving files from folder directory
@app.route('/<path:filename>')
def serve_file(filename):
    if 'logged_in' not in session:
        return redirect('/login')

    decoded_filename = unquote(filename)
    return send_from_directory(folderpath, decoded_filename, as_attachment=False)

#making file links in subdirectory    
@app.route('/folder/<path:subfolder>')
def subfolder_index(subfolder):
    if 'logged_in' not in session:
        return redirect('/login')

    folder_path = os.path.join(folderpath, subfolder)

    files = []
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)

    file_links = []

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        is_directory = os.path.isdir(file_path)

        if is_directory:
            file_links.append({'filename': filename, 'path': f'/folder/{subfolder}/{filename}', 'is_folder': True})
        else:
            file_links.append({'filename': filename, 'path': f'/folder/{subfolder}/{filename}', 'is_folder': False})

    return render_template('folder_index.html', files=file_links)

    
@app.route('/folder/<path:subfolder>/<path:nested_subfolder>/<path:filename>')
@app.route('/folder/<path:subfolder>/<path:filename>')
def serve_file_or_subfolder(subfolder, filename, nested_subfolder=''):
    if 'logged_in' not in session:
        return redirect('/login')

    folder_path = os.path.join(folderpath, subfolder, nested_subfolder)

    decoded_filename = unquote(filename)

    if os.path.isdir(os.path.join(folder_path, decoded_filename)):
        # Render subfolder index
        files = os.listdir(os.path.join(folder_path, decoded_filename))
        file_links = []

        for file in files:
            file_path = os.path.join(folder_path, decoded_filename, file)
            is_directory = os.path.isdir(file_path)

            if is_directory:
                file_links.append({'filename': file, 'path': f'/folder/{subfolder}/{nested_subfolder}/{decoded_filename}/{file}', 'is_folder': True})
            else:
                file_links.append({'filename': file, 'path': f'/folder/{subfolder}/{nested_subfolder}/{decoded_filename}/{file}', 'is_folder': False})

        return render_template('folder_index.html', files=file_links)
    else:
        # Serve file
        return send_from_directory(folder_path, decoded_filename, as_attachment=False)


@app.route('/launch-program')
def launch_program():
    return redirect('/sudopwd')

@app.route('/sudopwd', methods=['GET', 'POST'])
def sudopwd():
    if request.method == 'POST':
        password1 = request.form['sudopwd']

        # Set the sudo password in the session
        session['sudopwd'] = password1

        return redirect('/execute-command')

    return render_template('sudopwd.html')

@app.route('/execute-command')
def execute_command():
    if 'sudopwd' not in session:
        return redirect('/sudopwd')

    command1 = ['./network.sh', 'up']
    source_dir = fabric_dir   
    password1 = session.get('sudopwd', '')
    
        
   
@app.errorhandler(404)
def page_not_found(error):
    print("Error 404 Encountered")
    return render_template('errors.html', error_message='Page not found'), 404

        
if __name__== '__main__':
    app.run('0.0.0.0', port=9000)
    print("server is running at http://localhost:9000")
