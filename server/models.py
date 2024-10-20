from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
import re

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name') 
    def validate_name(self, key, name):
        existing_author = db.session.query(Author).filter_by(name=name).first()
        if existing_author is not None:
            raise ValueError(f"Author with the name '{name}' already exists.")
        if not name:
            raise ValueError("Author must have a name.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not re.fullmatch(r'\d{10}', phone_number):
            raise ValueError("Phone number must be 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if not category in valid_categories:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        content = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in content):
            raise ValueError("Title must contain one of the following phrases: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return title
        
        



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'