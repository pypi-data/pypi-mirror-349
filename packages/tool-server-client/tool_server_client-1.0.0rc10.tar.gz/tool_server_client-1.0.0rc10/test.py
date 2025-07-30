from src.tool_server_client.client import new_computer_use_client

if __name__ == "__main__":
    cli = new_computer_use_client("http://localhost:8102")
    res = cli.execute_command(command="ls", timeout = 10, check_session = 1)
    print(res)
