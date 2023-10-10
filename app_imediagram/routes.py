from flask import  render_template, url_for, redirect, request,send_from_directory
from app_imediagram import app, bcrypt, database
from app_imediagram.forms import FormLogin, FormCriarConta, FormFoto
from flask_login import login_required, login_user, logout_user, current_user
from app_imediagram.models import Usuario, Foto
from sqlalchemy import text
from werkzeug.utils import secure_filename
import uuid as uuid

import os


@app.route('/login', methods = [ "GET", "POST" ] )
def login():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        
        usuario = Usuario.query.filter_by( email = formlogin.email.data ).first()
        if usuario and bcrypt.check_password_hash( usuario.senha, formlogin.senha.data ):
            login_user( usuario )
            return redirect( url_for( "homepage" ,id_usuario = usuario.id) )

    return render_template( 'login.html', form = formlogin )

@app.route('/register', methods = [ "GET", "POST" ] )
def register():
    reisterForm = FormCriarConta()
    if reisterForm.is_submitted():
        photo = request.files['foto_perfil']
        photo_filename = secure_filename(photo.filename)
        photo_name = str(uuid.uuid1()) + "_" + photo_filename
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], photo_name )

        photo.save(caminho)
        
        senha = bcrypt.generate_password_hash( reisterForm.senha.data )
        usuario = Usuario( username = reisterForm.username.data, senha = senha, email = reisterForm.email.data, foto_perfil=photo_name )
        database.session.add( usuario )
        database.session.commit()

        login_user( usuario, remember = True )

        return redirect( url_for( "perfil", id_usuario = usuario.id ) )

    return render_template( 'register.html', form = reisterForm )

@app.route('/', methods = [ "GET" ])
@login_required
def homepage():
    if current_user.id:
        sql = text("select foto.imagem, usuario.username, usuario.foto_perfil from foto join usuario on usuario.id=foto.id_usuario")
        results = database.session.execute(sql)
        posts = []
        for r in results:
            posts.append(r)
        fotos = Foto.query.order_by( Foto.data_criacao.desc() ).all()
        return render_template( "homepage.html", usuario = current_user, posts=posts)
    else:
        return redirect( url_for( "login" ) )

@app.route( '/logout' )
@login_required
def logout():
    logout_user()
    return redirect( url_for( "login" ) )

@app.route( '/create-post', methods = [ "GET", "POST" ] )
@login_required
def createPost():
    if current_user.id:
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            photo = request.files['foto']
            photo_filename = secure_filename(photo.filename)
            photo_name = str(uuid.uuid1()) + "_" + photo_filename
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], photo_name )
            print(caminho)
        
            photo.save(caminho)

            foto = Foto( imagem = photo_name, id_usuario = current_user.id )
            database.session.add( foto )
            database.session.commit()

        return render_template( "create_post.html", form = formfoto )
    else:
        return redirect( url_for( "login" ) )

@app.route('/perfil/<id_usuario>', methods = [ "GET", "POST" ])
@login_required
def perfil( id_usuario ):

    if int( id_usuario ) == int( current_user.id ):
        formfoto = FormFoto()
        fotos = Foto.query.filter_by(id_usuario=current_user.id).all()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            caminho = os.path.join( app.config['UPLOAD_FOLDER'], arquivo )

            arquivo.save( caminho )

            foto = Foto( imagem = arquivo, id_usuario = current_user.id )
            database.session.add( foto )
            database.session.commit()

        return render_template( "perfil.html", usuario = current_user, form = formfoto,fotos=fotos )
    else:
        usuario = Usuario.query.get( int( id_usuario ) )
        return render_template( 'perfil.html', usuario = usuario, form = None, )
    
    
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    
    
