import os
import uuid

import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=openai.api_key)


# Database model
class BlogPost(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)


# Create tables
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        prompt = request.form['prompt']

        # Use OpenAI's chat.completions.create() to generate content
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative assistant helping to write engaging blog posts."},
                {"role": "user", "content": prompt}
            ]
        )
        content = completion.choices[0].message.content
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('show_post', post_id=new_post.id))
    return render_template('index.html')


@app.route('/posts/<post_id>')
def show_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts')
def list_posts():
    posts = BlogPost.query.all()
    return render_template('list_posts.html', posts=posts)


@app.route('/clear_data')
def clear_data():
    BlogPost.query.delete()
    db.session.commit()
    return "Data has been cleared from BlogPost."


if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
