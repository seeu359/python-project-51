# Page-loader


### Hexlet tests and linter status:
[![Actions Status](https://github.com/seeu359/python-project-51/workflows/hexlet-check/badge.svg)](https://github.com/seeu359/python-project-51/actions)
<a href="https://codeclimate.com/github/seeu359/python-project-51/maintainability"><img src="https://api.codeclimate.com/v1/badges/6e2c7754ff1825bb3231/maintainability" /></a>
[![code-check](https://github.com/seeu359/python-project-51/actions/workflows/lint_and_pytest_check.yml/badge.svg)](https://github.com/seeu359/python-project-51/actions/workflows/lint_and_pytest_check.yml)
<a href="https://codeclimate.com/github/seeu359/python-project-51/test_coverage"><img src="https://api.codeclimate.com/v1/badges/6e2c7754ff1825bb3231/test_coverage" /></a>

---

### Description:

A console utility that allows you to download a web page to a specified path on 
the pc with all its local resources. The resources are downloaded to a separate
folder.


### Installation: 
Clone repository by following command and run 'make install command'   
``$ git clone https://github.com/seeu359/python-project-51.git``


### Instruction:
To download the page, after installing the package, type the command 
``page-loader`` in the terminal, then specify the link to the downloaded page. 
Without specifying the path, the page will be downloaded to the current
directory. **Example:** 
>```$ page-loader https://test-site.com```

### Arguments:

1. **-o, --output** - ``~ page-loader <link> -o path/to/directory`` - 
specify the path to download webpage.
2. **-h, --help** - ``~ page-loader -h`` - shows a prompt.


---

[![asciicast](https://asciinema.org/a/VTMO3mWmbA7uCHaWLAoERzn3L.svg)](https://asciinema.org/a/VTMO3mWmbA7uCHaWLAoERzn3L)

[![asciicast](https://asciinema.org/a/529561.svg)](https://asciinema.org/a/529561)