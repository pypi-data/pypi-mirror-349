# LISA GW Response

LISA GW Response is a Python package computing the instrumental response to gravitational-waves, and produce a gravitational-wave (GW) file compatible with [LISA Instrument](https://gitlab.in2p3.fr/lisa-simulation/instrument) and [LISANode](https://gitlab.in2p3.fr/j2b.bayle/LISANode).

## Contributing

### Report an issue

We use the issue-tracking management system associated with the project provided by Gitlab. If you want to report a bug or request a feature, open an issue at <https://gitlab.in2p3.fr/lisa-simulation/gw-response/-/issues>. You may also thumb-up or comment on existing issues.

### Development environment

We strongly recommend to use [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

To setup the development environment, use the following commands:

```shell
git clone git@gitlab.in2p3.fr:lisa-simulation/gw-response.git
cd gw-response
python -m venv .
source ./bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

### Workflow

The project's development workflow is based on the issue-tracking system provided by Gitlab, as well as peer-reviewed merge requests. This ensures high-quality standards.

Issues are solved by creating branches and opening merge requests. Only the assignee of the related issue and merge request can push commits on the branch. Once all the changes have been pushed, the "draft" specifier on the merge request is removed, and the merge request is assigned to a reviewer. He can push new changes to the branch, or request changes to the original author by re-assigning the merge request to them. When the merge request is accepted, the branch is merged onto master, deleted, and the associated issue is closed.

### Pylint and Pytest

We enforce [PEP 8 (Style Guide for Python Code)](https://www.python.org/dev/peps/pep-0008/) with Pylint syntax checking, and correction of the code using the [pytest](https://docs.pytest.org/) testing framework. Both are implemented in the continuous integration system.

You can run them locally

```shell
pylint lisagwresponse/*.py
python -m pytest
```

## Use policy

The project is distributed under the 3-Clause BSD open-source license to foster open science in our community and share common tools. Please keep in mind that developing and maintaining such a tool takes time and effort. Therefore, we kindly ask you to

* Cite the DOI (see badge above) in any publication
* Acknowledge the authors (below)
* Acknowledge the LISA Simulation Expert Group in any publication

Do not hesitate to send an email to the authors for support. We always appreciate being associated with research projects.

## Authors

* Jean-Baptiste Bayle (<j2b.bayle@gmail.com>)
* Quentin Baghi (<quentin.baghi@cea.fr>)
* Arianna Renzini (<arenzini@caltech.edu>)
* Maude Le Jeune (<lejeune@apc.in2p3.fr>)
