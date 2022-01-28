all = development

development:
	uvicorn src.main:app --reload

clean:
	pyclean .

lint:
	mypy src

test:
	pytest -v