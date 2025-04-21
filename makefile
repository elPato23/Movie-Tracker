unit-test:
	pytest tests/unit --cov=tracker --cov-report=html --cov-report=xml --cov-report=term --html=htmlcov/report.html
int-test:
	pytest tests/unit --cov=tracker --cov-report=html --cov-report=xml --cov-report=term --html=htmlcov/report.html
test:
	pytest tests --cov=tracker --cov-report=html --cov-report=xml --cov-report=term --html=htmlcov/report.html
doc:
	pdoc tracker
render-cov:
	python -m http.server -d htmlcov 8080
start-api:
	python -m tracker.api
lint:
	black .
install-all:
	make install
	make install-dev
install:
	pip install -r requirements.txt
install-dev:
	pip install -r requirements-dev.txt
