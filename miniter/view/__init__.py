def create_endpoints(app, services):
    user_service = service.user_service

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        new_user    = request.json
        new_user_id = user_service.create_new_user(new_user)
        new_user    = user_serivce.get_user(new_user_id)

        return jsonify(new_user)
