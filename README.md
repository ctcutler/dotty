# dotty
Manage dots on Kanban boards

# setup
```
virtualenv -p python3 venv
. venv/bin/activate
make init
```

# run
```
python -m dotty <config_file>
```

# make targets
- `make init`: load requirements
- `make tests`: run tests
- `make install`: install dotty
- `make develop`: install dotty for development
- `make uninstall`: uninstall dotty
