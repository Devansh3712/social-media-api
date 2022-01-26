PY = python

all = development

development:
	uvicorn src.main:app --reload

production:
	uvicorn src.main:app

clean:
	pyclean .

lint:
	mypy src