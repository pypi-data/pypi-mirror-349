#!/usr/bin/env python3
import json
import smtplib
import ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import argparse
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Default configuration
DEFAULT_PORT = 8080
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Create directory for storing OAuth tokens if it doesn't exist
CONFIG_DIR = os.path.expanduser('~/.aws/amazonq/.email_mcp')
os.makedirs(CONFIG_DIR, exist_ok=True)

TOKEN_PATH = os.path.join(CONFIG_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(CONFIG_DIR, 'credentials.json')

class MCPHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            request = json.loads(post_data.decode('utf-8'))
            
            # Print request for debugging
            print(f"DEBUG: Received request to {self.path}: {json.dumps(request)}")
            
            print(f"Received request: {json.dumps(request, indent=2)}")
            
            if self.path == '/mcp/v1/tools':
                # Return tool definitions
                response = {
                    "tools": [
                        {
                            "name": "mbrug.email-mcp-server___send_email",
                            "description": "Send an email to the specified recipient using Gmail OAuth 2.0",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "to": {
                                        "type": "string",
                                        "description": "Email address of the recipient"
                                    },
                                    "subject": {
                                        "type": "string",
                                        "description": "Subject of the email"
                                    },
                                    "body": {
                                        "type": "string",
                                        "description": "Content of the email"
                                    }
                                },
                                "required": ["to", "subject", "body"]
                            }
                        },
                        {
                            "name": "mbrug.email-mcp-server___setup_oauth",
                            "description": "Setup OAuth 2.0 credentials for Gmail",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "credentials_path": {
                                        "type": "string",
                                        "description": "Path to the OAuth 2.0 credentials JSON file from Google Cloud Console"
                                    }
                                },
                                "required": ["credentials_path"]
                            }
                        }
                    ]
                }
                self._set_headers()
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == '/mcp/v1/invoke':
                tool_name = request.get("name")
                print(f"DEBUG: Received tool name: {tool_name}")
                
                # Log the full request for debugging
                with open(os.path.expanduser('~/tool_request_debug.log'), 'a') as f:
                    f.write(f"[{datetime.datetime.now()}] Received tool request: {json.dumps(request, indent=2)}\n")
                
                # Accept both formats for backward compatibility
                if tool_name and (tool_name == "email___send_email" or tool_name.endswith("___send_email")):
                    try:
                        print(f"DEBUG: Processing send_email request with parameters: {request.get('parameters', {})}")
                        result = self.send_email(request.get("parameters", {}))
                        response = {
                            "result": result
                        }
                        self._set_headers()
                        self.wfile.write(json.dumps(response).encode())
                        print(f"DEBUG: Successfully processed send_email request")
                    except Exception as e:
                        print(f"DEBUG: Error processing send_email request: {str(e)}")
                        error_response = {
                            "error": {
                                "message": str(e)
                            }
                        }
                        self._set_headers(400)
                        self.wfile.write(json.dumps(error_response).encode())
                elif tool_name and (tool_name == "email___setup_oauth" or tool_name.endswith("___setup_oauth") or tool_name == "setup_oauth"):
                    try:
                        result = self.setup_oauth(request.get("parameters", {}))
                        response = {
                            "result": result
                        }
                        self._set_headers()
                        self.wfile.write(json.dumps(response).encode())
                    except Exception as e:
                        error_response = {
                            "error": {
                                "message": str(e)
                            }
                        }
                        self._set_headers(400)
                        self.wfile.write(json.dumps(error_response).encode())
                else:
                    error_response = {
                        "error": {
                            "message": f"Unknown tool: {tool_name}"
                        }
                    }
                    self._set_headers(400)
                    self.wfile.write(json.dumps(error_response).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": {"message": "Not found"}}).encode())
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": {"message": f"Internal server error: {str(e)}"}}).encode())

    def get_gmail_service(self):
        """Get authenticated Gmail API service."""
        creds = None
        
        # Check if token file exists
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        
        # If credentials don't exist or are invalid, ask user to authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_PATH):
                    raise ValueError(f"OAuth credentials not found. Please run setup_oauth first.")
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        
        return build('gmail', 'v1', credentials=creds)

    def setup_oauth(self, params):
        """Setup OAuth 2.0 credentials."""
        credentials_path = params.get("credentials_path")
        
        if not credentials_path:
            raise ValueError("Missing required parameter: credentials_path")
        
        if not os.path.exists(os.path.expanduser(credentials_path)):
            raise ValueError(f"Credentials file not found at {credentials_path}")
        
        # Copy credentials to standard location
        with open(os.path.expanduser(credentials_path), 'r') as src:
            with open(CREDENTIALS_PATH, 'w') as dst:
                dst.write(src.read())
        
        # Try to authenticate to verify credentials
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Save the credentials
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
        
        return {
            "success": True,
            "message": "OAuth 2.0 credentials set up successfully. You can now use send_email."
        }

    def send_email(self, params):
        """Send an email using Gmail API with OAuth 2.0."""
        # Get parameters
        to_email = params.get("to")
        subject = params.get("subject")
        body = params.get("body")
        
        # Validate parameters
        if not to_email or not subject or not body:
            raise ValueError("Missing required parameters: to, subject, and body are required")
        
        try:
            service = self.get_gmail_service()
            
            # Create message
            message = MIMEMultipart()
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            # Encode the message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send the message
            message_object = service.users().messages().send(
                userId="me", 
                body={"raw": raw_message}
            ).execute()
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email}",
                "message_id": message_object.get("id")
            }
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

def run_server(port=DEFAULT_PORT):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPHandler)
    print(f"Starting MCP server on port {port}...")
    print(f"To use this server with Amazon Q CLI, run:")
    print(f"q config add-mcp-server email http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Email Server with OAuth 2.0")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to run the server on (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    
    run_server(args.port)
