from app.models import Category

def inject_categories():
    return {'get_categories': Category.get_all} 