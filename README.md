
## Install for use
Highly recommend using pipx over pip: https://pypa.github.io/pipx/ 
If you don't want to hack on it and just want to use it, you can install it with pipx.  
This will install it in a virtual environment and add it to your path.  
You can then run `gitgus` from anywhere.

```shell
brew install pipx && pipx ensurepath
pipx install git+https://github.com/mgfreshour/gitgus
gitgus config init global
cd "$EVERGAGE_SOURCE_ROOT"
gitgus config init local
```

## Install for development 
```shell
git clone git@github.com:mgfreshour/gitgus.git
cd gitgus
brew install sfdx
pipx install poetry
make deps lint test build install
```
