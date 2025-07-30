from gbb_excel_mcp.gbb import search
from gbb_excel_mcp.pro_suit_dify import difySuit
from gbb_excel_mcp.pro_collect_dify import difyCollect
from mcp.server import Server
from mcp import tool
import sys
import json

class GbbSearchServer(Server):
    def __init__(self):
        super().__init__("GbbSearchServer")
        
        @tool(name="工邦邦商品查询", description="根据商品描述，找出满足条件的商品编码")
        def suitProWithKey(key: str):
            """
            工邦邦商品查询工具
            
            根据用户输入的商品描述关键词，查询匹配的商品编码。
            """
            print("key:"+key)
            search_list = search(key)
            skuNo = difySuit(key, search_list)
            if skuNo == "":
                newKey = difyCollect(key)
                new_search_list = search(newKey)
                skuNo = difySuit(newKey, search_list)
            return {"skuNo": skuNo}
            
        self.add_tool(suitProWithKey)

def main():
    server = GbbSearchServer()
    while True:
        try:
            # 从stdin读取请求
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            response = server.handle_request(request)
            
            # 写入stdout响应
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
