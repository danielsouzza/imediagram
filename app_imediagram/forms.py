from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app_imediagram.models import Usuario

class FormLogin( FlaskForm ):
    email = StringField("E-mail", validators = [ DataRequired(), Email() ] )
    senha = PasswordField("Senha", validators = [ DataRequired() ] )
    botao_confirmacao = SubmitField("Fazer login")
class FormCriarConta( FlaskForm ):
    foto_perfil = FileField("Foto de perfil", validators=[ DataRequired() ])
    username = StringField("Nome de usuário", validators = [ DataRequired() ] )
    email = StringField("E-mail", validators = [ DataRequired(), Email() ] )
    senha = PasswordField("Senha", validators = [ DataRequired(), Length( 6, 20 ) ] )
    confirmacao_senha = PasswordField("Confirmação de senha", validators = [ DataRequired(), EqualTo( senha ) ] )
    
    botao_confirmacao = SubmitField("Criar conta")

    def validate_email(self, email ):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError( "E-mail já cadastrado. Proceda para o login!" )

class FormFoto( FlaskForm ):
    foto = FileField( "Foto", validators = [ DataRequired() ] )
    botao_confirmacao = SubmitField( "Enviar foto" )