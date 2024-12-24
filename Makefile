
buildtools:
	pip install uv

reqs: buildtools
	uv pip compile requirements.in -o requirements.txt

install: buildtools
	uv pip install -r requirements.txt

dev:
	python3 -m dash_app

prod:
	gunicorn dash_app:server --workers 4 --bind 0.0.0.0:8050
