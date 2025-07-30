from mcp_clp_server.server import mcp


def main():
    print('启动了')
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()