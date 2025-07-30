# Email MCP Server for Amazon Q

A custom MCP (Model Context Protocol) server that provides email functionality for Amazon Q CLI.

## Features

- Send emails using Gmail OAuth 2.0
- Secure authentication with Google's OAuth 2.0 flow
- Easy integration with Amazon Q CLI

## Installation

```bash
pip install mbrug-email-mcp-server
```

## Usage

### Setup OAuth 2.0 credentials

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Gmail API
3. Create OAuth 2.0 credentials (Desktop application)
4. Download the credentials JSON file
5. Run the setup command:

```bash
q tool mbrug.email-mcp-server___setup_oauth --credentials_path /path/to/credentials.json
```

### Send an email

```bash
q tool mbrug.email-mcp-server___send_email --to recipient@example.com --subject "Hello" --body "This is a test email"
```

## Running the server manually

If you need to run the server manually:

```bash
mbrug-email-mcp-server
```

Then configure Amazon Q to use it:

```bash
q config add-mcp-server email http://localhost:8080
```

## License

MIT
