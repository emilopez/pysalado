# PySalado

- Versión 1.0.0
- Ejemplo temporal en: https://emilopez-pysalado-webapp-mhmb0z.streamlitapp.com/


## Build installer

- Uso **pynsist**: https://pynsist.readthedocs.io/en/latest/index.html

Lo hago en windows a esto:

1. Get the tools. Install [NSIS](http://nsis.sourceforge.net/Download), and then install pynsist from PyPI by running `pip install pynsist`.

2. Armo este archivo de configurción `installer.cfg`:

```
[Application]
name=PySalado
version=1.0.0
# How to lunch the app - this calls the 'main' function from the 'run_app' package:
entry_point=src.run_app:main
#icon=resources/caritas-logo.ico

[Python]
version=3.8.10
bitness=64

[Include]
# Packages from PyPI that your application requires, one per line
# These must have wheels on PyPI:
pypi_wheels = altair==4.1.0
    astor==0.8.1
    attrs==21.2.0
    backcall==0.2.0
    backports.zoneinfo==0.2.1
    base58==2.1.0
    bleach==4.1.0
    blinker==1.5
    cachetools==4.2.2
    certifi==2021.5.30
    cffi==1.14.6
    charset-normalizer==2.0.6
    click==7.1.2
    decorator==5.1.0
    defusedxml==0.7.1
    distlib==0.3.3
    entrypoints==0.3
    idna==3.2
    jsonschema==3.2.0
    mistune==0.8.4
    mypy-extensions==0.4.3
    numpy==1.21.1
    packaging==21.0
    pandas==1.3.3
    pandocfilters==1.5.0
    parso==0.8.2
    pillow==8.3.2
    platformdirs==2.4.0
    prompt-toolkit==3.0.20
    protobuf==3.18.0
    pyarrow==5.0.0
    pycparser==2.20
    pydeck==0.7.0
    pyparsing==2.4.7
    pyrsistent==0.18.0
    python-dateutil==2.8.2
    pytz==2021.1
    requests==2.26.0
    requests-download==0.1.2
    send2trash==1.8.0
    setuptools==57.0.0
    six==1.14.0
    smmap==4.0.0
    streamlit==1.11.0
    terminado==0.12.1
    testpath==0.5.0
    toml==0.10.2
    tomli==1.2.1
    toolz==0.11.1
    tornado==6.1
    traitlets==5.1.0
    typing-extensions==3.10.0.2
    tzlocal==3.0
    urllib3==1.26.7
    validators==0.18.2
    # panda dependencies
    Jinja2==3.0.1
    # Jinja2 dependencies
    MarkupSafe==2.0.1
    # Plotly and its dependencies
    plotly==5.3.1
    tenacity==8.0.1

#extra_wheel_sources = ./wheels

files = src/datos/
```

3. Armo un directorio `src` donde alojo todo mi código del siguiente modo:
   -  `app.py`: Donde va a ir toooodo mi código de programa: streamlit + funciones, todo en uno!
   -  `run_app.py`: el script que va a ejecutar streamlit llamando a `app.py` 
   -  `__init__.py`: ya sabemos
   -  `datos`: directorio para almacenar `meta_estaciones_sah.csv` y `__init__.py`

4. Detalles a tener en cuenta en `app.py`
  - cuando se lee el archivo `meta_estaciones_sah.csv` hacerlo así: `os.path.join(os.path.dirname(__file__), "datos", "meta_estaciones_sah.csv")`

5. Finalmente ejecuto: `pynsist installer.cfg`
6. Generará un ejecutable `.exe` que es el único necesario para realizar la instalación. 


## Rutas de instalación
- Paquetes python: `C:\Users\emili\AppData\Local\pynsist\pypi\`
- Instalación de `PySalado.exe` en ruta: `C:\Users\emili\AppData\Local\Programs\PySalado\Python\`
