# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

APP_NAME=smackbang

env:
	API_KEY: ${{secrets.FLIGHT_DATA_TOKEN}}

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_keys:
	-@heroku keys:add ~/.ssh/id_ed25519.pub

heroku_create_app:
	-@heroku create --ssh-git ${APP_NAME} --region eu

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

destroy_heroku:
	-@heroku apps:destroy --app smackbang --confirm smackbang
