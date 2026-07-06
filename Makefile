PYTHON ?= python
PIP ?= pip

.PHONY: dev test migrate seed

dev:
	$(PYTHON) run.py

test:
	$(PYTHON) -m pytest -q

migrate:
	$(PYTHON) migrations/init_db.py

seed:
	$(PYTHON) -c "from app.search_space import SearchSpaceManager; SearchSpaceManager().load_pdfs_to_targets()"
