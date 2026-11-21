#!/usr/bin/env python3
"""Offline test of operator_bridge.py: a mock Telegram Bot API on 127.0.0.1 and a fake `claude`.

No bot, no token, no network beyond localhost, no model call.
Run: python -I test_operator_bridge.py   -> exit 0 and "ALL N CHECKS PASSED"
"""
import json
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = "123456:TESTtokenTESTtokenTESTtoken_x"
OWNER, STRANGER = 1111, 2222
passed = 0
sent: list[tuple[str, dict]] = []
queue: list[dict] = []


def check(cond, what):
    global passed
    if not cond:
        print("FAIL:", what)
        sys.exit(1)
    passed += 1
    print("ok  ", what)


class Mock(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        method = self.path.rsplit("/", 1)[-1]
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        ctype = self.headers.get("Content-Type", "")
        params = json.loads(body or b"{}") if "json" in ctype else {"_multipart_bytes": len(body),
                                                                       "_has_png": b"\x89PNG" in body}
        assert self.path.startswith(f"/bot{TOKEN}/"), self.path
        if method == "getUpdates":
            result = queue[:]
            queue.clear()
        else:
            sent.append((method, params))
            result = {"message_id": len(sent)} if method.startswith("send") else True
        out = json.dumps({"ok": True, "result": result}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(out)


FAKE_CLAUDE = r'''
import json, os, sys
args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
tools = args[args.index("--allowedTools") + 1]
leak = any("TESTtoken" in v for v in os.environ.values())
with open(os.environ["FAKE_LOG"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"tools": tools, "resume": "--resume" in args, "leak": leak}) + "\n")
if "--resume" in args:
    out = {"answer": "Deleted notes.tmp (exit 0).", "needs_approval": False}
elif "delete" in prompt.lower():
    out = {"answer": "That changes a file.", "needs_approval": True, "proposed_action": "Delete notes.tmp in the workdir"}
else:
    out = {"answer": "You have 3 files in the folder.", "needs_approval": False}
print(json.dumps({"type": "result", "is_error": False, "session_id": "s-1", "total_cost_usd": 0.01,
                  "result": json.dumps(out), "structured_output": out}))
'''


def msg(uid, chat, text, ctype="private"):
    return {"update_id": uid, "message": {"message_id": uid, "date": 0, "text": text,
                                          "from": {"id": chat}, "chat": {"id": chat, "type": ctype}}}


def button(uid, chat, data, sender=None):
    return {"update_id": uid, "callback_query": {"id": f"cb{uid}", "data": data, "from": {"id": sender or chat},
                                                  "message": {"message_id": 1, "chat": {"id": chat, "type": "private"}}}}


srv = ThreadingHTTPServer(("127.0.0.1", 0), Mock)
threading.Thread(target=srv.serve_forever, daemon=True).start()

sys.path.insert(0, str(HERE))
import operator_bridge as ob  # noqa: E402

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    fake = d / "fake_claude.py"
    fake.write_text(FAKE_CLAUDE, encoding="utf-8")
    import os
    os.environ["FAKE_LOG"] = str(d / "fake.log")
    os.environ["BQ_TG_TOKEN_LEAK_TEST"] = TOKEN     # must not reach the child process
    env = d / "operator.env"
    env.write_text(f"BQ_TG_TOKEN={TOKEN}\nBQ_TG_ALLOWED_CHATS={OWNER}\nBQ_TG_API=http://127.0.0.1:{srv.server_port}\n"
                   f"BQ_OP_CLAUDE={fake}\nBQ_OP_WORKDIR={d}\nBQ_OP_AUDIT={d / 'audit.jsonl'}\n", encoding="utf-8")

    r = subprocess.run([sys.executable, "-I", str(HERE / "operator_bridge.py"), "--env", str(d / "missing.env")],
                       capture_output=True, text=True)
    check(r.returncode == 2, "missing env file -> exit 2")
    bad = d / "bad.env"
    bad.write_text(f"BQ_TG_TOKEN={TOKEN}\nBQ_TG_ALLOWED_CHATS=\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(HERE / "operator_bridge.py"), "--env", str(bad)],
                       capture_output=True, text=True)
    check(r.returncode == 2 and "serve nobody" in r.stderr, "empty allow-list -> refuses to start")

    b = ob.Bridge(ob.load_env(env))
    audit = lambda: [json.loads(l) for l in (d / "audit.jsonl").read_text(encoding="utf-8").splitlines()]

    queue.append(msg(1, STRANGER, "list my files"))
    queue.append(msg(2, OWNER, "list my files", ctype="group"))
    b.poll_once(0)
    check(not sent, "stranger and group chats get no reply at all")
    check([e["event"] for e in audit()].count("refused") == 2, "both refusals are in the audit log")

    queue.append(msg(3, OWNER, "how many files are in the folder?"))
    b.poll_once(0)
    texts = [p.get("text", "") for m, p in sent if m == "sendMessage"]
    check(any("3 files" in t for t in texts), "owner question -> answer sent back")
    calls = [json.loads(l) for l in (d / "fake.log").read_text(encoding="utf-8").splitlines()]
    check(calls[-1]["tools"] == ob.READ_TOOLS and not calls[-1]["resume"], "question ran with read-only tools")
    check(not any(c["leak"] for c in calls), "the token is not in the child process environment")

    sent.clear()
    queue.append(msg(4, OWNER, "delete notes.tmp"))
    b.poll_once(0)
    prop = [p for m, p in sent if m == "sendMessage" and "reply_markup" in p]
    check(len(prop) == 1 and "nothing done yet" in prop[0]["text"], "a change comes back as a proposal")
    data = prop[0]["reply_markup"]["inline_keyboard"][0][0]["callback_data"]
    check(data.startswith("ok:") and len(data.encode()) <= 64, "Approve button carries short callback_data (<= 64 bytes)")
    calls = [json.loads(l) for l in (d / "fake.log").read_text(encoding="utf-8").splitlines()]
    check(calls[-1]["tools"] == ob.READ_TOOLS and not calls[-1]["resume"], "the run that proposed the change was read-only")

    queue.append(button(5, OWNER, data, sender=STRANGER))
    b.poll_once(0)
    check(audit()[-1]["event"] == "refused_button", "a button press from a non-allowed user is refused")

    sent.clear()
    queue.append(button(6, OWNER, data))
    b.poll_once(0)
    calls = [json.loads(l) for l in (d / "fake.log").read_text(encoding="utf-8").splitlines()]
    check(calls[-1]["resume"] and "Write" in calls[-1]["tools"], "approved action runs once, resumed, with write tools")
    check(any("Deleted notes.tmp" in p.get("text", "") for m, p in sent if m == "sendMessage"), "result reported back")
    check(any(m == "answerCallbackQuery" for m, _ in sent), "every button press is answered (answerCallbackQuery)")

    sent.clear()
    queue.append(button(7, OWNER, data))
    b.poll_once(0)
    check(any("expired or was already decided" in p.get("text", "") for m, p in sent), "a second press is refused")

    events = [e["event"] for e in audit()]
    check(all(e in events for e in ("message", "run", "proposal", "decision")), "audit holds message, run, proposal, decision")
    check(TOKEN not in (d / "audit.jsonl").read_text(encoding="utf-8"), "the token never appears in the audit log")

    png = d / "x.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
    sent.clear()
    b.tg.send_file("sendPhoto", "photo", OWNER, png, "screen")
    check(sent and sent[-1][0] == "sendPhoto" and sent[-1][1]["_has_png"], "sendPhoto multipart upload reaches the API")

    shot = ob.screenshot(d / "shots" / "real.png")
    check(shot.exists() and shot.read_bytes()[:4] == b"\x89PNG", f"local screenshot captured ({shot.stat().st_size} bytes)")

srv.shutdown()
print(f"ALL {passed} CHECKS PASSED")
