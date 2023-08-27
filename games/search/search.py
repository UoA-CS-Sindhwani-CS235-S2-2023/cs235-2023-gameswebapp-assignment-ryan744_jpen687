from flask import Blueprint, request, redirect, url_for

search_blueprint = Blueprint(
    'search_bp', __name__)

@search_blueprint.route('/search', methods=['POST'])
def submitSearch():
    form_data = request.form
    return redirect(url_for(
        'games_bp.browse_all_games',
        page=1,
        search_term=form_data['searchTerm'],
        search_category=form_data['searchCategory'],
    ))