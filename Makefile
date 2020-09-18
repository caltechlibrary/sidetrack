# =============================================================================
# @file    Makefile
# @brief   Makefile for some steps in creating new releases on GitHub
# @author  Michael Hucka
# @date    2020-08-11
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/sidetrack
# =============================================================================

# Before we go any further, test if certain programs are available.
# The following is based on the approach by Jonathan Ben-Avraham posted to
# Stack Overflow in 2014 at https://stackoverflow.com/a/25668869

PROGRAMS_NEEDED = gh jq
TEST := $(foreach p,$(PROGRAMS_NEEDED),\
	  $(if $(shell which $(p)),_,$(error Cannot find program "$(p)")))

# Gather values that we need further below.

name	 := $(shell grep 'name\s*=' setup.cfg | cut -f2 -d'=' | tr -d '[:blank:]')
version	 := $(shell grep 'version\s*=' setup.cfg | cut -f2 -d'=' | tr -d '[:blank:]')
branch	 := $(shell git rev-parse --abbrev-ref HEAD)
repo	 := $(shell gh repo view | head -1 | cut -f2 -d':' | tr -d '[:blank:]')
id	 := $(shell curl -s https://api.github.com/repos/$(repo) | jq '.id')
doi_url	 := $(shell curl -sILk https://data.caltech.edu/badge/latestdoi/$(id) | grep Locat | cut -f2 -d' ')
doi	 := $(subst https://doi.org/,,$(doi_url))
doi_tail := $(lastword $(subst ., ,$(doi)))
tempfile := $(shell mktemp /tmp/release-notes-$(name).XXXXXX)

# The main action is "make release".

release: | test-branch release-on-github print-instructions

test-branch:
ifneq ($(branch),main)
	$(error Current git branch != main. Merge changes into main first)
endif

release-on-github:;
	sed -i .bak -e "/version/ s/[0-9].[0-9].[0-9]/$(version)/" codemeta.json
	git add codemeta.json
	git diff-index --quiet HEAD codemeta.json || git commit -m"Update version number" codemeta.json
	git push -v --all
	git push -v --tags
	$(info ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓)
	$(info ┃ Write release notes in the file that will be opened in your editor ┃)
	$(info ┃ then save and close the file to complete this release process.     ┃)
	$(info ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛)
	sleep 2
	$(EDITOR) $(tempfile)
	gh release create v$(version) -d -t "Release $(version)" -F $(tempfile)

print-instructions:;
	$(info ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓)
	$(info ┃ Next steps:                                                        ┃)
	$(info ┃ 1. Visit https://github.com/$(repo)/releases )
	$(info ┃ 2. Double-check the draft release, and click "Publish" if ready    ┃)
	$(info ┃ 3. Wait a few seconds to let web services do their work            ┃)
	$(info ┃ 4. Run "make update-doi" to update the DOI in README.md            ┃)
	$(info ┃ 5. Run "make create-dist" and check the distribution for problems  ┃)
	$(info ┃ 6. Run "make test-pypi" to push to test.pypi.org                   ┃)
	$(info ┃ 7. Double-check https://test.pypi.org/$(repo) )
	$(info ┃ 8. Run "make pypi" to push to pypi for real                        ┃)
	$(info ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛)
	@echo ""

update-doi: 
	sed -i .bak -e 's|DOI-.*-blue|DOI-$(doi)-blue|' README.md
	sed -i .bak -e 's|caltech.edu/records/[0-9]\{1,\}|caltech.edu/records/$(doi_tail)|' README.md
	git add README.md
	git diff-index --quiet HEAD README.md || git commit -m"Update DOI" README.md && git push -v --all

create-dist: clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine check dist/*

test-pypi:;
	python3 -m twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*

pypi: create-dist
	python3 -m twine upload --verbose dist/*

clean:;
	-rm -rf dist build $(name).egg-info

.PHONY: release release-on-github print-instructions clean test-pypi pypi
