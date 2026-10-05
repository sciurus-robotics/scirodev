# Sourced by the scripts here: put a working Python environment on PATH and
# make sure it has what the scripts need. Not meant to be run on its own.
#
# The virtual environment is, in this order:
#   $SCIRODEV_VENV          if set
#   ../.venv                when this checkout sits inside a parent project that has one
#   ./.venv                 otherwise (created on first use)
#
# Then this package (editable) and its docs extra (Sphinx, furo) are installed
# if they are missing, so a freshly recreated environment just works.

_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -n "${SCIRODEV_VENV:-}" ]; then
  _venv="$SCIRODEV_VENV"
elif [ -f "$_root/../.venv/bin/activate" ]; then
  _venv="$_root/../.venv"
else
  _venv="$_root/.venv"
fi

if [ ! -f "$_venv/bin/activate" ]; then
  echo ">> creating virtual environment $_venv"
  python3 -m venv "$_venv"
fi
# shellcheck disable=SC1091
source "$_venv/bin/activate"

if ! python -c 'import sphinx, furo, pybricksdev, scirodev, sciro' 2>/dev/null; then
  echo ">> installing scirodev and its docs requirements into $_venv"
  python -m pip install --quiet --disable-pip-version-check -e "$_root[docs]"
fi

unset _root _venv
