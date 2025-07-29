import click
from .core import setup_mcp


@click.command()
@click.option("--jwt-token", required=True, help="API认证令牌")
def main(jwt_token: str):
    mcp = setup_mcp(jwt_token)
    print('hefeng-weather启动成功')
    mcp.run()
