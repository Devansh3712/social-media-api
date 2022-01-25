PY = python

all = development

development:
	uvicorn main:app --reload

clean:
	pyclean .
