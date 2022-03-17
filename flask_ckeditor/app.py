from flask import Flask, render_template
from flask_ckeditor import CKEditor, CKEditorField

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.secret_key = 'secret string'

ckeditor = CKEditor(app)


class PostForm(FlaskForm):
  title = StringField('Title')
  body = CKEditorField('Body')
  submit = SubmitField('Submit')


class Get_The_Article():

  def __init__(self):
    self.title = "de Finibus Bonorum et Malorum - Part I"
    self.text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor \
                incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud \
                exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure \
                dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. \
                Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt \
                mollit anim id est laborum."


def get_the_article():
  return Get_The_Article()


@app.route('/', methods=['GET', 'POST'])
def index():
  form = PostForm()
  if form.validate_on_submit():
    title = form.title.data
    body = form.body.data
    return render_template('post.html', title=title, body=body)
  article_body = get_the_article()
  return render_template('index.html', article_body=article_body, form=form)


if __name__ == '__main__':
  app.run()
