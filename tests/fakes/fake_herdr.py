import json,socket,os,sys
p=sys.argv[1]
if os.path.exists(p): os.unlink(p)
s=socket.socket(socket.AF_UNIX); s.bind(p); s.listen(5)
log=open(sys.argv[2] if len(sys.argv)>2 else os.devnull,"w")
SCREEN="""● Update(model/forecast.py)
  ⎿  Updated model/forecast.py
     12 -horizon = 12
     12 +horizon = 24
     13 +dropout = 0.2
 Do you want to make this edit to forecast.py?
 ❯ 1. Yes
   2. Yes, allow all edits during this session (shift+tab)
   3. No, and tell Claude what to do differently (esc)"""
while True:
    c,_=s.accept(); m=json.loads(c.makefile().readline()); log.write(json.dumps(m)+"\n"); log.flush()
    if m["method"]=="agent.list":
        r={"type":"agent_list","agents":[
          {"terminal_id":"t1","name":"api-refactor","agent":"claude","agent_status":"working","workspace_id":"w1","tab_id":"w1:t1","pane_id":"w1:p1","focused":False,"revision":1,"cwd":os.path.expanduser("~/easyfin")},
          {"terminal_id":"t2","name":"tcc-forecast","agent":"claude","agent_status":"blocked","workspace_id":"w2","tab_id":"w2:t1","pane_id":"w2:p1","focused":False,"revision":1},
          {"terminal_id":"t3","agent":"codex","agent_status":"done","workspace_id":"w3","tab_id":"w3:t1","pane_id":"w3:p1","focused":True,"revision":1}]}
    elif m["method"]=="agent.read":
        txt=SCREEN if m["params"]["target"]=="tcc-forecast" else "line a\n\nline b\nline c\nline d\nline e"
        r={"type":"agent_read","read":{"pane_id":"x","workspace_id":"w","tab_id":"t","source":m["params"]["source"],"format":"text","text":txt,"revision":1,"truncated":False}}
    else: r={"type":"ok"}
    c.sendall((json.dumps({"id":m["id"],"result":r})+"\n").encode()); c.close()
