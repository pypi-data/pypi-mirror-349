from lp_tool_mcp.app import mcp


def main():
    print('lp-tool-mcp 启动了')
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()