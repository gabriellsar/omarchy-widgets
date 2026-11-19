import json,sys,os
for line in sys.stdin:
    m=json.loads(line)
    if "id" not in m: continue
    meth=m["method"]
    if meth=="initialize": r={"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"serverInfo":{"name":"fake","version":"0"}}
    elif meth=="tools/list": r={"tools":[{"name":"get_open_positions","description":"Open positions"},{"name":"get_account","description":"acct"}]}
    elif meth=="tools/call":
        if m["params"]["name"]=="get_open_positions":
            data={"data":{"items":[{"instrument":"btc","direction":"Buy","amount":"0.35","openPrice":88120,"price":92410.5,"pl":1501.68},{"instrument":"ETH","direction":"Sell","amount":2,"openPrice":3410,"price":3322.4,"pl":175.2}]},"key":os.environ.get("QUANTFURY_API_KEY")}
            r={"content":[{"type":"text","text":json.dumps(data)}]}
        else: r={"content":[],"structuredContent":{"balance":{"equity":"48,210.37"}}}
    print("log line not json", flush=True)
    print(json.dumps({"jsonrpc":"2.0","id":m["id"],"result":r}),flush=True)
