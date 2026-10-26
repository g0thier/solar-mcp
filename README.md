# Solar MCP

## Description

Solar MCP enables you to retrieve information about the UV index and ozone levels for a given location. It's designed to provide accurate and timely environmental data for developers and researchers.

Solar MCP is based on the previous project [Solaire API](https://github.com/g0thier/Solaire-API), adapted from FastAPI to FastMCP.

![Capture](/docs/images/Capture.png)

## Table of Contents

- [Solar MCP](#solar-mcp)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [🎯 Objective of the project](#-objective-of-the-project)
  - [👥 Target audience](#-target-audience)
  - [⚙️ What this repository includes](#️-what-this-repository-includes)
  - [🗂️ Repository structure](#️-repository-structure)
  - [🚀 Quick start](#-quick-start)
  - [🐳 Install \& execute](#-install--execute)
  - [🧪 Test with MCP Inspector](#-test-with-mcp-inspector)
  - [🥽 Security](#-security)
  - [📰 Changelog](#-changelog)
  - [🩷 Acknowledgements](#-acknowledgements)
    - [Environnement](#environnement)
  - [🧪 Project Status](#-project-status)
  - [🔒 License](#-license)
  - [🤝 Contributing](#-contributing)
  - [👤 Author](#-author)

## 🎯 Objective of the project

The main goal of this project is to provide an easy-to-use API that allows users to access UV index and ozone level data based on geographic coordinates. This can be particularly useful for developers building applications related to weather, health, or environmental monitoring. By offering a simple interface to retrieve this information, we aim to facilitate the integration of environmental data into various applications and services.

## 👥 Target audience 

- Developers building applications that require environmental data
- Health professionals interested in UV exposure and ozone levels
- Researchers in environmental science
- Data scientists interested in environmental data

## ⚙️ What this repository includes

- `.gitignore` for macOS configuration
- Core community files:
  - `CODE_OF_CONDUCT.md`
  - `CONTRIBUTING.md`
  - `SECURITY.md`
  - `CHANGELOG.md`
  - `LICENSE.md`
  - `ACKNOWLEDGEMENTS.md`
- FastMCP application in `fastmcp/app/` with:
  - `main.py` to run the API
  - `custom.py` for API logic and utilities
  - `index.html` for the API homepage
- Example Jupyter notebook in `notebooks/`
- Basic documentation assets in `docs/`
- MCP Inspector configuration in `test/mcp.json`

## 🗂️ Repository structure

```text

solar-mcp/
├── .gitignore
├── docs/
│   └── images/
├── fastmcp/
│   ├── app/
│   │   ├── custom.py
│   │   ├── index.html
│   │   └── main.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── notebooks/
│   └── notebooks.ipynb
├── test/
│   └── mcp.json
├── ACKNOWLEDGEMENTS.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE.md
├── README.md
└── SECURITY.md
```

## 🚀 Quick start

To quickly get started with the Solar MCP, you can use Docker to set up and run the application. The MCP endpoint is `http://localhost:80/mcp`, exposing the `get_uv_week` tool with optional `longitude` and `latitude` arguments (defaults: `6.132936441`, `46.220473615`).

To set up the application, ensure you have Docker installed and follow these steps:

1. Start the application using Docker Compose:
   ```shell
   cd fastmcp
   docker compose up
   ```
2. Access the API homepage in your browser at:
   ```
   http://localhost:80
   ```

## 🐳 Install & execute

For use the `fastmcp/` app:

```bash
pip install -r fastmcp/requirements.txt
cd fastmcp/app
uvicorn main:app --reload
```

For this local command, connect your MCP client to `http://localhost:8000/mcp`.

## 🧪 Test with MCP Inspector

Prerequisites: Docker with Docker Compose, and Node.js ≥ 22.19.0 with npm/npx.
Run both commands from the repository root, in separate terminals.

1. Start Solar MCP and leave it running:

   ```bash
   docker compose -f fastmcp/docker-compose.yml up --build
   ```

2. Start MCP Inspector with the supplied configuration:

   ```bash
   npx @modelcontextprotocol/inspector@2.12.0 --config test/mcp.json
   ```

3. Open the browser URL printed by Inspector. The `solar-mcp` server is already configured with **Streamable HTTP** at `http://localhost:80/mcp`, without authentication or custom headers. Enable its connection toggle.
4. Open **Tools**, select **get_uv_week**, and run it with the default coordinates, or enter `longitude: 7.4474` and `latitude: 46.948` for Bern.
5. Inspect the JSON result: `longitude`, `latitude`, and an `infos` array containing `date`, `uv_index`, and `ozone` for each day. The first call may take longer while Solar MCP downloads the TEMIS data.

Inspector reads `test/mcp.json` without modifying it when launched with `--config`; see the [Inspector v2 documentation](https://github.com/modelcontextprotocol/inspector/blob/main/docs/v1-to-v2-migration.md#--config-vs---catalog).

## 🥽 Security

- See [SECURITY.md](/SECURITY.md) for vulnerability reporting guidelines.

## 📰 Changelog

Track all notable project changes in [CHANGELOG.md](/CHANGELOG.md).

Recommended:
- Follow a consistent format such as Keep a Changelog
- Create an entry for each release
- Include Added, Changed, Fixed, and Removed sections when relevant

## 🩷 Acknowledgements

- Use [ACKNOWLEDGEMENTS.md](/ACKNOWLEDGEMENTS.md) to credit people, tools, libraries, and communities that helped the project.

### Environnement

- **Python ≥ 3.13.5**
- Dependencies listed in [requirements.txt](/fastmcp/requirements.txt)

## 🧪 Project Status

- 🔬 **Statut** : experimental
- 🧭 **Roadmap** : to be defined

## 🔒 License

- See [LICENSE.md](/LICENSE.md).

## 🤝 Contributing

Contributions are welcome.
- See [CONTRIBUTING.md](/CONTRIBUTING.md)
- Code of conduct available in [CODE_OF_CONDUCT.md](/CODE_OF_CONDUCT.md).

## 👤 Author

Gauthier Rammault
