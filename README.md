
## Install for use
Highly recommend using pipx over pip: https://pypa.github.io/pipx/ `brew install pipx && pipx ensurepath`
If you don't want to hack on it and just want to use it, you can install it with pipx.  
This will install it in a virtual environment and add it to your path.  
You can then run `gitgus` from anywhere.

```shell
mkdir -p ~/.config/pip
curl -o ~/.config/pip/pip.conf https://git.soma.salesforce.com/pages/python-at-sfdc/python-guide/pip-conf/pip.conf
curl -o ~/.config/pip/cert.pem https://git.soma.salesforce.com/pages/python-at-sfdc/python-guide/pip-conf/cert.pem
pip install git+ssh://git@git.soma.salesforce.com/mfreshour/gitgus.git
```

_NOTE: You'll need to have SSH keys setup for git.soma.salesforce.com._

_NOTE: This uses internal packages, be sure to [configure your local machine](https://git.soma.salesforce.com/pages/python-at-sfdc/python-guide/package-indexes/#configure-your-local-machine) before installing._

## Install for development 
```shell
brew install sfdx
pipx install poetry
mkdir -p ~/.config/pip
curl -o ~/.config/pip/pip.conf https://git.soma.salesforce.com/pages/python-at-sfdc/python-guide/pip-conf/pip.conf
curl -o ~/.config/pip/cert.pem https://git.soma.salesforce.com/pages/python-at-sfdc/python-guide/pip-conf/cert.pem
poetry source add sfdc "https://ops0-artifactrepo1-0-prd.data.sfdc.net/artifactory/api/pypi/python-certified/simple/"
poetry config certificates.sfdc.cert ~/.config/pip/cert.pem
make 
```
