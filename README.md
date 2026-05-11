## File Manager

![Screamshot](image.png)

A cross-platform desktop and web file manager built with Python and [Flet](https://flet.dev/).
Runs natively on Windows, macOS, Linux, Android, iOS, and as a web app — all from a single codebase.

## Tech stack
- **Python** - Core languge
- **Flet** - cross-platform UI framework
- **pip** - fast Python package manager

## Features

- Browse and navigate local file system
- Cross-platform: desktop, mobile, and web from same codebase
- Ligthweiht and fast startup with `pip`

## Get Started

### Prerequisites

- Python 3.11+
- [pip](https://pypi.org/project/pip/) installed

### Installation

clone the repository

```bash
git clone https://github.com/bayronrc/file_manager.git
cd file_manager
```
create a virtual enviroment `venv`:
```bash
python -m venv .venv
```
Linux
```bash
source venv/bin/activate
```

Windows
```bash
.\venv\Scripts\activate
```
install the dependences

```bash
pip install - r requirements.txt
```
### Run

```bash
#desktop
flet run

# web app
flet run -w

# watch changes
flet run -r
```
## build

| Platform | Command |
|----------|---------|
| Android  | `flet build apk -v` |
| iOS      | `flet build ipa -v` |
| Windows  | `flet build windows -v` |
| macOS    | `flet build macos -v` |
| Linux    | `flet build linux -v` |
| Web      | `flet build web -v` |


For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/).

## Project Sctruture

```bash
file_manager/
├── src/          # Application source code
├── requirements.txt
└── pyproject.toml
└── .gitignore
```

## Licence

MIT
