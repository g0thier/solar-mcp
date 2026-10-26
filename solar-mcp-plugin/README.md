# Solar MCP — archive de plugin

Cette archive référence le serveur Solar MCP déployé sur Render.

- Dépôt déclaré : https://github.com/g0thier/solar-mcp
- Serveur déclaré : https://solar-mcp.onrender.com
- URL MCP configurée : https://solar-mcp.onrender.com/mcp

## Créer l’archive ZIP

Depuis la racine du dépôt, exécuter :

```sh
(cd solar-mcp-plugin && zip -r ../solar-mcp-plugin.zip plugin.json mcp.json README.md assets -x '*.DS_Store' '__MACOSX/*')
```

Cette commande place les manifestes à la racine de l’archive et exclut les fichiers macOS.

## Installation

1. Importer l'archive ZIP dans une interface qui autorise l'import de plugins.
2. Si une étape de connexion MCP apparaît, renseigner l'URL MCP publique exacte.
3. Tester avec : « Compare les indices UV à Madrid, Londres et Mahé. »
