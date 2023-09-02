#!/usr/bin/env bash
set -e

PYTHON_VERSION=3.11.5
TK_PREFIX=$(brew --prefix tcl-tk)
V=$(brew info tcl-tk | head -1 | cut -d' ' -f4 | cut -d'.' -f1,2)

env \
  PATH="$TK_PREFIX/bin:$PATH" \
  LDFLAGS="-L$TK_PREFIX/lib" \
  CPPFLAGS="-I$TK_PREFIX/include" \
  PKG_CONFIG_PATH="$TK_PREFIX/lib/pkgconfig" \
  CFLAGS="-I$TK_PREFIX/include" \
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$TK_PREFIX/include' --with-tcltk-libs='-L$TK_PREFIX/lib -ltcl$V -ltk$V'" \
  pyenv install $PYTHON_VERSION

pyenv global $PYTHON_VERSION
pip install --upgrade pip
pip install poetry

