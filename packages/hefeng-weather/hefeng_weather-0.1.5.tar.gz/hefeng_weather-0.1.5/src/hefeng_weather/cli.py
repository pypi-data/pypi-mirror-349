import click
from .core import setup_mcp


@click.command()
@click.option("--token", required=True, help="API认证令牌")
@click.option("--host", required=True, help="API主机地址")
def main(token: str, host: str):
    """启动 hefeng-weather 服务"""
    mcp = setup_mcp(token, host)
    print('hefeng-weather启动成功')
    mcp.run()


if __name__ == "__main__":
    main()
