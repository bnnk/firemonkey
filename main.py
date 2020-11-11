import os
import fnmatch as fn
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

POSTS = {}
for markdown_post in fn.filter(os.listdir('content'),"*.page"):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])
POSTS = {
    post: POSTS[post] \
    for post in sorted(
        POSTS,
        key=lambda post: datetime.strptime(
            POSTS[post].metadata['date'], '%Y-%m-%d'
        ),
        reverse=True
    )
}
        
env = Environment(loader=PackageLoader('main', 'templates'))
index_template = env.get_template('home.html')
post_template = env.get_template('post.html')

index_posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in index_posts_metadata]

index_html_content = index_template.render(posts=index_posts_metadata)
with open('output/index.html', 'w') as file:
    file.write(index_html_content)

# render each post and write it to output/posts/<post.slug>/index.html
for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
    }

    post_html_content = post_template.render(post=post_data)

    post_file_path = 'output/posts/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html_content)
