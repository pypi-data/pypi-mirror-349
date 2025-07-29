import argparse
import os

from dotenv import load_dotenv

from .server.mcp_server import TraceNexusServer


def main():
    """Main entry point for the CLI."""
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="TraceNexus: MCP server for LLM tracing platforms"
    )
    parser.add_argument(
        "--transport",
        choices=["streamable-http"],
        default="streamable-http",
        help="Transport protocol (only streamable-http is supported)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the HTTP server (used with streamable-http transport)",
    )
    parser.add_argument(
        "--mount-path",
        type=str,
        default="/mcp",
        help="Path to mount the MCP endpoints (used with streamable-http transport)",
    )

    args = parser.parse_args()

    langsmith_api_key = os.environ.get("LANGSMITH_API_KEY", "example")
    langsmith_project = os.environ.get("LANGSMITH_PROJECT", "example")

    print(f"INFO: LANGSMITH_API_KEY found (first 5 chars: {langsmith_api_key[:5]})")
    if langsmith_api_key.lower() == "example":
        print(
            "WARNING: LANGSMITH_API_KEY is set to 'example'. "
            "This is a placeholder and will likely not work. Please set a valid API key or unset the variable if not using LangSmith."
        )

    print(f"INFO: LANGSMITH_PROJECT found (first 5 chars: {langsmith_project[:5]})")
    if langsmith_project.lower() == "example":
        print(
            "WARNING: LANGSMITH_PROJECT is set to 'example'. "
            "This is a placeholder and may not be desired. Please set a valid project name or unset the variable if not using LangSmith."
        )

    langfuse_public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "example")
    langfuse_secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "example")

    print(f"INFO: LANGFUSE_PUBLIC_KEY found (first 5 chars: {langfuse_public_key[:5]})")
    if langfuse_public_key.lower() == "example":
        print(
            "WARNING: LANGFUSE_PUBLIC_KEY is set to 'example'. "
            "This is a placeholder and will likely not work. Please set a valid public key or unset the variable if not using Langfuse."
        )

    print(f"INFO: LANGFUSE_SECRET_KEY found (first 5 chars: {langfuse_secret_key[:5]})")
    if langfuse_secret_key.lower() == "example":
        print(
            "WARNING: LANGFUSE_SECRET_KEY is set to 'example'. "
            "This is a placeholder and will likely not work. Please set a valid secret key or unset the variable if not using Langfuse."
        )

    server = TraceNexusServer()
    server.run(transport=args.transport, port=args.port, mount_path=args.mount_path)


if __name__ == "__main__":
    main()
