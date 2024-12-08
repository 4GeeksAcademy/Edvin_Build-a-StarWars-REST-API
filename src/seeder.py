from app import app, db
from models import Users, Articles, Tags, ArticlesTags

def seed_users():
    users = [
        Users(email='test1@test.com', password='test123', is_active=True),
        Users(email='test2@test.com', password='test123', is_active=True),
        Users(email='test3@test.com', password='test123', is_active=True)
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()

def seed_tags():
    tags = [
        Tags(name='Pyhton'),
        Tags(name='Flask'),
        Tags(name='SQLAlchemy')
    ]

    db.session.bulk_save_objects(tags)
    db.session.commit()

def seed_articles():
    articles = [
        Articles(title='First Article', content='Content of the first article', user_id=1),
        Articles(title='Second Article', content='Content of the second article', user_id=2),
        Articles(title='Third Article', content='Content of the third article', user_id=3)
    ]
    db.session.bulk_save_objects(articles)
    db.session.commit()

def seed_article_tags():
    article_tags = [
        ArticlesTags(article_id=1, tag_id=1, extra_info='Extra info 1'),
        ArticlesTags(article_id=2, tag_id=2, extra_info='Extra info 2'),
        ArticlesTags(article_id=3, tag_id=3, extra_info='Extra info 3')
    ]
    db.session.bulk_save_objects(article_tags)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_users()
        seed_tags()
        seed_articles()
        seed_article_tags()
        print("Database seeded!")
