import dataclasses
import typing
import algosdk
from algosdk.transaction import OnComplete
from algosdk.atomic_transaction_composer import TransactionSigner
from algosdk.source_map import SourceMap
from algosdk.transaction import Transaction
from algosdk.v2client.models import SimulateTraceConfig
import algokit_utils
from algokit_utils import AlgorandClient as _AlgoKitAlgorandClient

_APP_SPEC_JSON = r"""{"arcs": [22, 28], "bareActions": {"call": ["DeleteApplication", "NoOp", "UpdateApplication"], "create": ["DeleteApplication", "NoOp"]}, "methods": [{"actions": {"call": [], "create": ["NoOp"]}, "args": [], "name": "create", "returns": {"type": "string"}, "desc": "Initialize the contract with creator as admin.", "events": [], "readonly": false, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [{"type": "address", "name": "student"}], "name": "mint_initial", "returns": {"type": "string"}, "desc": "Initialize a student with 0 score (creates box storage).", "events": [], "readonly": false, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [{"type": "address", "name": "student"}, {"type": "uint64", "name": "points"}], "name": "add_reputation", "returns": {"type": "string"}, "desc": "Add reputation points to a student (admin only).", "events": [], "readonly": false, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [{"type": "address", "name": "student"}], "name": "get_score", "returns": {"type": "uint64"}, "desc": "Get reputation score for a student.", "events": [], "readonly": true, "recommendations": {}}, {"actions": {"call": ["NoOp"], "create": []}, "args": [], "name": "get_admin", "returns": {"type": "address"}, "desc": "Get the admin address.", "events": [], "readonly": true, "recommendations": {}}], "name": "HustleScore", "state": {"keys": {"box": {}, "global": {"admin": {"key": "YWRtaW4=", "keyType": "AVMString", "valueType": "address"}}, "local": {}}, "maps": {"box": {"scores": {"keyType": "address", "valueType": "uint64", "prefix": "c2NvcmVz"}}, "global": {}, "local": {}}, "schema": {"global": {"bytes": 1, "ints": 0}, "local": {"bytes": 0, "ints": 0}}}, "structs": {}, "byteCode": {"approval": "CyADAQAgJgMFYWRtaW4Gc2NvcmVzBBUffHUxG0EAOzEZFEQxGEEAJIIEBHYs6PsEfU0wrQQgW3IMBDRrPbw2GgCOBABHAI4A0QDvAIAE1uhxTTYaAI4BAA8AIjEZkIExGkQoMQBnIkMoMQBngCEVH3x1ABtIdXN0bGVTY29yZSBTQlQgaW5pdGlhbGl6ZWSwIkM2GgFJFSQSRDEAIyhlRBJEKUxQSb5IFxREIxa/gCYVH3x1ACBTdHVkZW50IGluaXRpYWxpemVkIHdpdGggMCBzY29yZbAiQzYaAUkVJBJENhoCSRWBCBJEFzEAIyhlRBJEKU8CUEm+TBdETwIIFr+AFhUffHUAEFJlcHV0YXRpb24gYWRkZWSwIkM2GgFJFSQSRClMUL5MF0AACCMWKkxQsCJDSRZC//UjKGVEKkxQsCJD", "clear": "C4EBQw=="}, "desc": "\n    Hustle Score SBT for CampusNexus\n    \n    Features:\n    - Non-transferable (soulbound)\n    - Per-student score stored in BoxMap\n    - Score increases with completed projects\n    - Admin-managed score updates\n    ", "events": [], "networks": {}, "source": {"approval": "I3ByYWdtYSB2ZXJzaW9uIDExCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuYXBwcm92YWxfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIGludGNibG9jayAxIDAgMzIKICAgIGJ5dGVjYmxvY2sgImFkbWluIiAic2NvcmVzIiAweDE1MWY3Yzc1CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjEwCiAgICAvLyBjbGFzcyBIdXN0bGVTY29yZShBUkM0Q29udHJhY3QpOgogICAgdHhuIE51bUFwcEFyZ3MKICAgIGJ6IG1haW5fYmFyZV9yb3V0aW5nQDE1CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBieiBtYWluX2NyZWF0ZV9Ob09wQDExCiAgICBwdXNoYnl0ZXNzIDB4NzYyY2U4ZmIgMHg3ZDRkMzBhZCAweDIwNWI3MjBjIDB4MzQ2YjNkYmMgLy8gbWV0aG9kICJtaW50X2luaXRpYWwoYWRkcmVzcylzdHJpbmciLCBtZXRob2QgImFkZF9yZXB1dGF0aW9uKGFkZHJlc3MsdWludDY0KXN0cmluZyIsIG1ldGhvZCAiZ2V0X3Njb3JlKGFkZHJlc3MpdWludDY0IiwgbWV0aG9kICJnZXRfYWRtaW4oKWFkZHJlc3MiCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBtaW50X2luaXRpYWwgYWRkX3JlcHV0YXRpb24gZ2V0X3Njb3JlIGdldF9hZG1pbgogICAgZXJyCgptYWluX2NyZWF0ZV9Ob09wQDExOgogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weToxMAogICAgLy8gY2xhc3MgSHVzdGxlU2NvcmUoQVJDNENvbnRyYWN0KToKICAgIHB1c2hieXRlcyAweGQ2ZTg3MTRkIC8vIG1ldGhvZCAiY3JlYXRlKClzdHJpbmciCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAwCiAgICBtYXRjaCBjcmVhdGUKICAgIGVycgoKbWFpbl9iYXJlX3JvdXRpbmdAMTU6CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjMxCiAgICAvLyBAYmFyZW1ldGhvZChjcmVhdGU9ImFsbG93IiwgYWxsb3dfYWN0aW9ucz1bIk5vT3AiLCAiVXBkYXRlQXBwbGljYXRpb24iLCAiRGVsZXRlQXBwbGljYXRpb24iXSkKICAgIGludGNfMCAvLyAxCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBzaGwKICAgIHB1c2hpbnQgNDkKICAgICYKICAgIGFzc2VydAogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTozNC0zNgogICAgLy8gIyBEdXJpbmcgY3JlYXRpb24sIGFkbWluIGlzIHNldC4gRm9yIHVwZGF0ZS9kZWxldGUsIHdlIGFsbG93IChjb21tZW50ZWQgb3V0IGFkbWluIGNoZWNrIGZvciBub3cpCiAgICAvLyAjIE5vIGV4cGxpY2l0IGNoZWNrIG5lZWRlZCAtIGFsZ29weSByb3V0aW5nIGhhbmRsZXMgQXBwbGljYXRpb25JRCBzZW1hbnRpY3MKICAgIC8vIHNlbGYuYWRtaW4udmFsdWUgPSBUeG4uc2VuZGVyCiAgICBieXRlY18wIC8vICJhZG1pbiIKICAgIHR4biBTZW5kZXIKICAgIGFwcF9nbG9iYWxfcHV0CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjMxCiAgICAvLyBAYmFyZW1ldGhvZChjcmVhdGU9ImFsbG93IiwgYWxsb3dfYWN0aW9ucz1bIk5vT3AiLCAiVXBkYXRlQXBwbGljYXRpb24iLCAiRGVsZXRlQXBwbGljYXRpb24iXSkKICAgIGludGNfMCAvLyAxCiAgICByZXR1cm4KCgovLyBzbWFydF9jb250cmFjdHMuaHVzdGxlX3Njb3JlLmNvbnRyYWN0Lkh1c3RsZVNjb3JlLmNyZWF0ZVtyb3V0aW5nXSgpIC0+IHZvaWQ6CmNyZWF0ZToKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9odXN0bGVfc2NvcmUvY29udHJhY3QucHk6MjgKICAgIC8vIHNlbGYuYWRtaW4udmFsdWUgPSBUeG4uc2VuZGVyCiAgICBieXRlY18wIC8vICJhZG1pbiIKICAgIHR4biBTZW5kZXIKICAgIGFwcF9nbG9iYWxfcHV0CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjI1CiAgICAvLyBAYWJpbWV0aG9kKGNyZWF0ZT0icmVxdWlyZSIpCiAgICBwdXNoYnl0ZXMgMHgxNTFmN2M3NTAwMWI0ODc1NzM3NDZjNjU1MzYzNmY3MjY1MjA1MzQyNTQyMDY5NmU2OTc0Njk2MTZjNjk3YTY1NjQKICAgIGxvZwogICAgaW50Y18wIC8vIDEKICAgIHJldHVybgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5odXN0bGVfc2NvcmUuY29udHJhY3QuSHVzdGxlU2NvcmUubWludF9pbml0aWFsW3JvdXRpbmddKCkgLT4gdm9pZDoKbWludF9pbml0aWFsOgogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTozOAogICAgLy8gQGFiaW1ldGhvZCgpCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBkdXAKICAgIGxlbgogICAgaW50Y18yIC8vIDMyCiAgICA9PQogICAgYXNzZXJ0IC8vIGludmFsaWQgbnVtYmVyIG9mIGJ5dGVzIGZvciBhcmM0LnN0YXRpY19hcnJheTxhcmM0LnVpbnQ4LCAzMj4KICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9odXN0bGVfc2NvcmUvY29udHJhY3QucHk6NDEKICAgIC8vIGFzc2VydCBUeG4uc2VuZGVyID09IHNlbGYuYWRtaW4udmFsdWUsICJPbmx5IGFkbWluIGNhbiBtaW50IgogICAgdHhuIFNlbmRlcgogICAgaW50Y18xIC8vIDAKICAgIGJ5dGVjXzAgLy8gImFkbWluIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBzZWxmLmFkbWluIGV4aXN0cwogICAgPT0KICAgIGFzc2VydCAvLyBPbmx5IGFkbWluIGNhbiBtaW50CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjQzLTQ0CiAgICAvLyAjIENoZWNrIGlmIGFscmVhZHkgZXhpc3RzCiAgICAvLyBleGlzdHMsIF92YWwgPSBzZWxmLnNjb3Jlcy5tYXliZShzdHVkZW50KQogICAgYnl0ZWNfMSAvLyAic2NvcmVzIgogICAgc3dhcAogICAgY29uY2F0CiAgICBkdXAKICAgIGJveF9nZXQKICAgIHBvcAogICAgYnRvaQogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo0NQogICAgLy8gYXNzZXJ0IG5vdCBleGlzdHMsICJTdHVkZW50IGFscmVhZHkgaW5pdGlhbGl6ZWQiCiAgICAhCiAgICBhc3NlcnQgLy8gU3R1ZGVudCBhbHJlYWR5IGluaXRpYWxpemVkCiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjQ3LTQ4CiAgICAvLyAjIEluaXRpYWxpemUgd2l0aCAwCiAgICAvLyBzZWxmLnNjb3Jlc1tzdHVkZW50XSA9IFVJbnQ2NCgwKQogICAgaW50Y18xIC8vIDAKICAgIGl0b2IKICAgIGJveF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9odXN0bGVfc2NvcmUvY29udHJhY3QucHk6MzgKICAgIC8vIEBhYmltZXRob2QoKQogICAgcHVzaGJ5dGVzIDB4MTUxZjdjNzUwMDIwNTM3NDc1NjQ2NTZlNzQyMDY5NmU2OTc0Njk2MTZjNjk3YTY1NjQyMDc3Njk3NDY4MjAzMDIwNzM2MzZmNzI2NQogICAgbG9nCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgoKLy8gc21hcnRfY29udHJhY3RzLmh1c3RsZV9zY29yZS5jb250cmFjdC5IdXN0bGVTY29yZS5hZGRfcmVwdXRhdGlvbltyb3V0aW5nXSgpIC0+IHZvaWQ6CmFkZF9yZXB1dGF0aW9uOgogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo1MgogICAgLy8gQGFiaW1ldGhvZCgpCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBkdXAKICAgIGxlbgogICAgaW50Y18yIC8vIDMyCiAgICA9PQogICAgYXNzZXJ0IC8vIGludmFsaWQgbnVtYmVyIG9mIGJ5dGVzIGZvciBhcmM0LnN0YXRpY19hcnJheTxhcmM0LnVpbnQ4LCAzMj4KICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDIKICAgIGR1cAogICAgbGVuCiAgICBwdXNoaW50IDgKICAgID09CiAgICBhc3NlcnQgLy8gaW52YWxpZCBudW1iZXIgb2YgYnl0ZXMgZm9yIGFyYzQudWludDY0CiAgICBidG9pCiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjU1CiAgICAvLyBhc3NlcnQgVHhuLnNlbmRlciA9PSBzZWxmLmFkbWluLnZhbHVlLCAiT25seSBhZG1pbiBjYW4gYWRkIHJlcHV0YXRpb24iCiAgICB0eG4gU2VuZGVyCiAgICBpbnRjXzEgLy8gMAogICAgYnl0ZWNfMCAvLyAiYWRtaW4iCiAgICBhcHBfZ2xvYmFsX2dldF9leAogICAgYXNzZXJ0IC8vIGNoZWNrIHNlbGYuYWRtaW4gZXhpc3RzCiAgICA9PQogICAgYXNzZXJ0IC8vIE9ubHkgYWRtaW4gY2FuIGFkZCByZXB1dGF0aW9uCiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjU3LTU4CiAgICAvLyAjIEVuc3VyZSBzdHVkZW50IGlzIGluaXRpYWxpemVkCiAgICAvLyBleGlzdHMsIGN1cnJlbnRfc2NvcmUgPSBzZWxmLnNjb3Jlcy5tYXliZShzdHVkZW50KQogICAgYnl0ZWNfMSAvLyAic2NvcmVzIgogICAgdW5jb3ZlciAyCiAgICBjb25jYXQKICAgIGR1cAogICAgYm94X2dldAogICAgc3dhcAogICAgYnRvaQogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo1OQogICAgLy8gYXNzZXJ0IGV4aXN0cywgIlN0dWRlbnQgbm90IGluaXRpYWxpemVkIgogICAgYXNzZXJ0IC8vIFN0dWRlbnQgbm90IGluaXRpYWxpemVkCiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjYxLTYyCiAgICAvLyAjIFVwZGF0ZSBzY29yZQogICAgLy8gc2VsZi5zY29yZXNbc3R1ZGVudF0gPSBjdXJyZW50X3Njb3JlICsgcG9pbnRzCiAgICB1bmNvdmVyIDIKICAgICsKICAgIGl0b2IKICAgIGJveF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9odXN0bGVfc2NvcmUvY29udHJhY3QucHk6NTIKICAgIC8vIEBhYmltZXRob2QoKQogICAgcHVzaGJ5dGVzIDB4MTUxZjdjNzUwMDEwNTI2NTcwNzU3NDYxNzQ2OTZmNmUyMDYxNjQ2NDY1NjQKICAgIGxvZwogICAgaW50Y18wIC8vIDEKICAgIHJldHVybgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5odXN0bGVfc2NvcmUuY29udHJhY3QuSHVzdGxlU2NvcmUuZ2V0X3Njb3JlW3JvdXRpbmddKCkgLT4gdm9pZDoKZ2V0X3Njb3JlOgogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo2NgogICAgLy8gQGFiaW1ldGhvZChyZWFkb25seT1UcnVlKQogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQogICAgZHVwCiAgICBsZW4KICAgIGludGNfMiAvLyAzMgogICAgPT0KICAgIGFzc2VydCAvLyBpbnZhbGlkIG51bWJlciBvZiBieXRlcyBmb3IgYXJjNC5zdGF0aWNfYXJyYXk8YXJjNC51aW50OCwgMzI+CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjY5CiAgICAvLyBleGlzdHMsIHNjb3JlID0gc2VsZi5zY29yZXMubWF5YmUoc3R1ZGVudCkKICAgIGJ5dGVjXzEgLy8gInNjb3JlcyIKICAgIHN3YXAKICAgIGNvbmNhdAogICAgYm94X2dldAogICAgc3dhcAogICAgYnRvaQogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo3MAogICAgLy8gaWYgbm90IGV4aXN0czoKICAgIGJueiBnZXRfc2NvcmVfYWZ0ZXJfaWZfZWxzZUAzCiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjcxCiAgICAvLyByZXR1cm4gQVJDNFVJbnQ2NChVSW50NjQoMCkpCiAgICBpbnRjXzEgLy8gMAogICAgaXRvYgoKZ2V0X3Njb3JlX2FmdGVyX2lubGluZWRfc21hcnRfY29udHJhY3RzLmh1c3RsZV9zY29yZS5jb250cmFjdC5IdXN0bGVTY29yZS5nZXRfc2NvcmVANDoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy9odXN0bGVfc2NvcmUvY29udHJhY3QucHk6NjYKICAgIC8vIEBhYmltZXRob2QocmVhZG9ubHk9VHJ1ZSkKICAgIGJ5dGVjXzIgLy8gMHgxNTFmN2M3NQogICAgc3dhcAogICAgY29uY2F0CiAgICBsb2cKICAgIGludGNfMCAvLyAxCiAgICByZXR1cm4KCmdldF9zY29yZV9hZnRlcl9pZl9lbHNlQDM6CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5OjczCiAgICAvLyByZXR1cm4gQVJDNFVJbnQ2NChzY29yZSkKICAgIGR1cAogICAgaXRvYgogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo2NgogICAgLy8gQGFiaW1ldGhvZChyZWFkb25seT1UcnVlKQogICAgYiBnZXRfc2NvcmVfYWZ0ZXJfaW5saW5lZF9zbWFydF9jb250cmFjdHMuaHVzdGxlX3Njb3JlLmNvbnRyYWN0Lkh1c3RsZVNjb3JlLmdldF9zY29yZUA0CgoKLy8gc21hcnRfY29udHJhY3RzLmh1c3RsZV9zY29yZS5jb250cmFjdC5IdXN0bGVTY29yZS5nZXRfYWRtaW5bcm91dGluZ10oKSAtPiB2b2lkOgpnZXRfYWRtaW46CiAgICAvLyBzbWFydF9jb250cmFjdHMvaHVzdGxlX3Njb3JlL2NvbnRyYWN0LnB5Ojc4CiAgICAvLyByZXR1cm4gc2VsZi5hZG1pbi52YWx1ZQogICAgaW50Y18xIC8vIDAKICAgIGJ5dGVjXzAgLy8gImFkbWluIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBzZWxmLmFkbWluIGV4aXN0cwogICAgLy8gc21hcnRfY29udHJhY3RzL2h1c3RsZV9zY29yZS9jb250cmFjdC5weTo3NQogICAgLy8gQGFiaW1ldGhvZChyZWFkb25seT1UcnVlKQogICAgYnl0ZWNfMiAvLyAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgaW50Y18wIC8vIDEKICAgIHJldHVybgo=", "clear": "I3ByYWdtYSB2ZXJzaW9uIDExCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBhbGdvcHkuYXJjNC5BUkM0Q29udHJhY3QuY2xlYXJfc3RhdGVfcHJvZ3JhbSgpIC0+IHVpbnQ2NDoKbWFpbjoKICAgIHB1c2hpbnQgMQogICAgcmV0dXJuCg=="}, "sourceInfo": {"approval": {"pcOffsetMethod": "none", "sourceInfo": [{"pc": [242], "errorMessage": "Only admin can add reputation"}, {"pc": [161], "errorMessage": "Only admin can mint"}, {"pc": [170], "errorMessage": "Student already initialized"}, {"pc": [251], "errorMessage": "Student not initialized"}, {"pc": [159, 240, 317], "errorMessage": "check self.admin exists"}, {"pc": [153, 224, 291], "errorMessage": "invalid number of bytes for arc4.static_array<arc4.uint8, 32>"}, {"pc": [233], "errorMessage": "invalid number of bytes for arc4.uint64"}]}, "clear": {"pcOffsetMethod": "none", "sourceInfo": []}}, "templateVariables": {}}"""
APP_SPEC = algokit_utils.Arc56Contract.from_json(_APP_SPEC_JSON)

def _parse_abi_args(args: object | None = None) -> list[object] | None:

    if args is None:
        return None

    def convert_dataclass(value: object) -> object:
        if dataclasses.is_dataclass(value):
            return tuple(convert_dataclass(getattr(value, field.name)) for field in dataclasses.fields(value))
        elif isinstance(value, (list, tuple)):
            return type(value)(convert_dataclass(item) for item in value)
        return value

    match args:
        case tuple():
            method_args = list(args)
        case _ if dataclasses.is_dataclass(args):
            method_args = [getattr(args, field.name) for field in dataclasses.fields(args)]
        case _:
            raise ValueError("Invalid 'args' type. Expected 'tuple' or 'TypedDict' for respective typed arguments.")

    return [
        convert_dataclass(arg) if not isinstance(arg, algokit_utils.AppMethodCallTransactionArgument) else arg
        for arg in method_args
    ] if method_args else None

def _init_dataclass(cls: type, data: dict) -> object:

    field_values = {}
    for field in dataclasses.fields(cls):
        field_value = data.get(field.name)
        if dataclasses.is_dataclass(field.type) and isinstance(field_value, dict):
            field_values[field.name] = _init_dataclass(typing.cast(type, field.type), field_value)
        else:
            field_values[field.name] = field_value
    return cls(**field_values)

@dataclasses.dataclass(frozen=True, kw_only=True)
class MintInitialArgs:

    student: str

    @property
    def abi_method_signature(self) -> str:
        return "mint_initial(address)string"

@dataclasses.dataclass(frozen=True, kw_only=True)
class AddReputationArgs:

    student: str
    points: int

    @property
    def abi_method_signature(self) -> str:
        return "add_reputation(address,uint64)string"

@dataclasses.dataclass(frozen=True, kw_only=True)
class GetScoreArgs:

    student: str

    @property
    def abi_method_signature(self) -> str:
        return "get_score(address)uint64"

class _HustleScoreUpdate:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def bare(
        self, params: algokit_utils.AppClientBareCallParams | None = None
    ) -> algokit_utils.AppUpdateParams:
        return self.app_client.params.bare.update(params)

class _HustleScoreDelete:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def bare(
        self, params: algokit_utils.AppClientBareCallParams | None = None
    ) -> algokit_utils.AppCallParams:
        return self.app_client.params.bare.delete(params)

class HustleScoreParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    @property
    def update(self) -> "_HustleScoreUpdate":
        return _HustleScoreUpdate(self.app_client)

    @property
    def delete(self) -> "_HustleScoreDelete":
        return _HustleScoreDelete(self.app_client)

    def mint_initial(
        self,
        args: tuple[str] | MintInitialArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "mint_initial(address)string",
            "args": method_args,
        }))

    def add_reputation(
        self,
        args: tuple[str, int] | AddReputationArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "add_reputation(address,uint64)string",
            "args": method_args,
        }))

    def get_score(
        self,
        args: tuple[str] | GetScoreArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_score(address)uint64",
            "args": method_args,
        }))

    def get_admin(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_admin()address",
        }))

    def create(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.AppCallMethodCallParams:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.params.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "create()string",
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> algokit_utils.AppCallParams:
        return self.app_client.params.bare.clear_state(
            params,
            
        )

class _HustleScoreUpdateTransaction:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def bare(self, params: algokit_utils.AppClientBareCallParams | None = None) -> Transaction:
        return self.app_client.create_transaction.bare.update(params)

class _HustleScoreDeleteTransaction:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def bare(self, params: algokit_utils.AppClientBareCallParams | None = None) -> Transaction:
        return self.app_client.create_transaction.bare.delete(params)

class HustleScoreCreateTransactionParams:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    @property
    def update(self) -> "_HustleScoreUpdateTransaction":
        return _HustleScoreUpdateTransaction(self.app_client)

    @property
    def delete(self) -> "_HustleScoreDeleteTransaction":
        return _HustleScoreDeleteTransaction(self.app_client)

    def mint_initial(
        self,
        args: tuple[str] | MintInitialArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "mint_initial(address)string",
            "args": method_args,
        }))

    def add_reputation(
        self,
        args: tuple[str, int] | AddReputationArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "add_reputation(address,uint64)string",
            "args": method_args,
        }))

    def get_score(
        self,
        args: tuple[str] | GetScoreArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_score(address)uint64",
            "args": method_args,
        }))

    def get_admin(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_admin()address",
        }))

    def create(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> algokit_utils.BuiltTransactions:
    
        params = params or algokit_utils.CommonAppCallParams()
        return self.app_client.create_transaction.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "create()string",
        }))

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        
    ) -> Transaction:
        return self.app_client.create_transaction.bare.clear_state(
            params,
            
        )

class _HustleScoreUpdateSend:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def bare(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.SendAppTransactionResult:
        return self.app_client.send.bare.update(
            params=params,
            send_params=send_params,
            compilation_params=compilation_params
        )

class _HustleScoreDeleteSend:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    def bare(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        
    ) -> algokit_utils.SendAppTransactionResult:
        return self.app_client.send.bare.delete(
            params=params,
            send_params=send_params,
            
        )

class HustleScoreSend:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    @property
    def update(self) -> "_HustleScoreUpdateSend":
        return _HustleScoreUpdateSend(self.app_client)

    @property
    def delete(self) -> "_HustleScoreDeleteSend":
        return _HustleScoreDeleteSend(self.app_client)

    def mint_initial(
        self,
        args: tuple[str] | MintInitialArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[str]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "mint_initial(address)string",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[str], parsed_response)

    def add_reputation(
        self,
        args: tuple[str, int] | AddReputationArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[str]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "add_reputation(address,uint64)string",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[str], parsed_response)

    def get_score(
        self,
        args: tuple[str] | GetScoreArgs,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[int]:
        method_args = _parse_abi_args(args)
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_score(address)uint64",
            "args": method_args,
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[int], parsed_response)

    def get_admin(
        self,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[str]:
    
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "get_admin()address",
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[str], parsed_response)

    def create(
        self,
        params: algokit_utils.CommonAppCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[str]:
    
        params = params or algokit_utils.CommonAppCallParams()
        response = self.app_client.send.call(algokit_utils.AppClientMethodCallParams(**{
            **dataclasses.asdict(params),
            "method": "create()string",
        }), send_params=send_params)
        parsed_response = response
        return typing.cast(algokit_utils.SendAppTransactionResult[str], parsed_response)

    def clear_state(
        self,
        params: algokit_utils.AppClientBareCallParams | None = None,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAppTransactionResult[algokit_utils.ABIReturn]:
        return self.app_client.send.bare.clear_state(
            params,
            send_params=send_params,
        )

class GlobalStateValue(typing.TypedDict):

    admin: str

class HustleScoreState:

    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client

    @property
    def global_state(
        self
    ) -> "_GlobalState":

            return _GlobalState(self.app_client)

    @property
    def box(
        self
    ) -> "_BoxState":

            return _BoxState(self.app_client)

class _GlobalState:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client
        
        self._struct_classes: dict[str, typing.Type[typing.Any]] = {}

    def get_all(self) -> GlobalStateValue:

        result = self.app_client.state.global_state.get_all()
        if not result:
            return typing.cast(GlobalStateValue, {})

        converted = {}
        for key, value in result.items():
            key_info = self.app_client.app_spec.state.keys.global_state.get(key)
            struct_class = self._struct_classes.get(key_info.value_type) if key_info else None
            converted[key] = (
                _init_dataclass(struct_class, value) if struct_class and isinstance(value, dict)
                else value
            )
        return typing.cast(GlobalStateValue, converted)

    @property
    def admin(self) -> str:

        value = self.app_client.state.global_state.get_value("admin")
        if isinstance(value, dict) and "address" in self._struct_classes:
            return _init_dataclass(self._struct_classes["address"], value)
        return typing.cast(str, value)

class _BoxState:
    def __init__(self, app_client: algokit_utils.AppClient):
        self.app_client = app_client
        
        self._struct_classes: dict[str, typing.Type[typing.Any]] = {}

    def get_all(self) -> dict[str, typing.Any]:

        result = self.app_client.state.box.get_all()
        if not result:
            return {}

        converted = {}
        for key, value in result.items():
            key_info = self.app_client.app_spec.state.keys.box.get(key)
            struct_class = self._struct_classes.get(key_info.value_type) if key_info else None
            converted[key] = (
                _init_dataclass(struct_class, value) if struct_class and isinstance(value, dict)
                else value
            )
        return converted

    @property
    def scores(self) -> "_MapState[str, int]":

        return _MapState(
            self.app_client.state.box,
            "scores",
            None
        )

_KeyType = typing.TypeVar("_KeyType")
_ValueType = typing.TypeVar("_ValueType")

class _AppClientStateMethodsProtocol(typing.Protocol):
    def get_map(self, map_name: str) -> dict[typing.Any, typing.Any]:
        ...
    def get_map_value(self, map_name: str, key: typing.Any) -> typing.Any | None:
        ...

class _MapState(typing.Generic[_KeyType, _ValueType]):

    def __init__(self, state_accessor: _AppClientStateMethodsProtocol, map_name: str,
                struct_class: typing.Type[_ValueType] | None = None):
        self._state_accessor = state_accessor
        self._map_name = map_name
        self._struct_class = struct_class

    def get_map(self) -> dict[_KeyType, _ValueType]:

        result = self._state_accessor.get_map(self._map_name)
        if self._struct_class and result:
            return {k: _init_dataclass(self._struct_class, v) if isinstance(v, dict) else v
                    for k, v in result.items()}
        return typing.cast(dict[_KeyType, _ValueType], result or {})

    def get_value(self, key: _KeyType) -> _ValueType | None:

        key_value = dataclasses.asdict(key) if dataclasses.is_dataclass(key) else key
        value = self._state_accessor.get_map_value(self._map_name, key_value)
        if value is not None and self._struct_class and isinstance(value, dict):
            return _init_dataclass(self._struct_class, value)
        return typing.cast(_ValueType | None, value)

class HustleScoreClient:

    @typing.overload
    def __init__(self, app_client: algokit_utils.AppClient) -> None: ...
    
    @typing.overload
    def __init__(
        self,
        *,
        algorand: _AlgoKitAlgorandClient,
        app_id: int,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> None: ...

    def __init__(
        self,
        app_client: algokit_utils.AppClient | None = None,
        *,
        algorand: _AlgoKitAlgorandClient | None = None,
        app_id: int | None = None,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> None:
        if app_client:
            self.app_client = app_client
        elif algorand and app_id:
            self.app_client = algokit_utils.AppClient(
                algokit_utils.AppClientParams(
                    algorand=algorand,
                    app_spec=APP_SPEC,
                    app_id=app_id,
                    app_name=app_name,
                    default_sender=default_sender,
                    default_signer=default_signer,
                    approval_source_map=approval_source_map,
                    clear_source_map=clear_source_map,
                )
            )
        else:
            raise ValueError("Either app_client or algorand and app_id must be provided")
    
        self.params = HustleScoreParams(self.app_client)
        self.create_transaction = HustleScoreCreateTransactionParams(self.app_client)
        self.send = HustleScoreSend(self.app_client)
        self.state = HustleScoreState(self.app_client)

    @staticmethod
    def from_creator_and_name(
        creator_address: str,
        app_name: str,
        algorand: _AlgoKitAlgorandClient,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
        ignore_cache: bool | None = None,
        app_lookup_cache: algokit_utils.ApplicationLookup | None = None,
    ) -> "HustleScoreClient":
        return HustleScoreClient(
            algokit_utils.AppClient.from_creator_and_name(
                creator_address=creator_address,
                app_name=app_name,
                app_spec=APP_SPEC,
                algorand=algorand,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
                ignore_cache=ignore_cache,
                app_lookup_cache=app_lookup_cache,
            )
        )
    
    @staticmethod
    def from_network(
        algorand: _AlgoKitAlgorandClient,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> "HustleScoreClient":
        return HustleScoreClient(
            algokit_utils.AppClient.from_network(
                app_spec=APP_SPEC,
                algorand=algorand,
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    @property
    def app_id(self) -> int:
        return self.app_client.app_id
    
    @property
    def app_address(self) -> str:
        return self.app_client.app_address
    
    @property
    def app_name(self) -> str:
        return self.app_client.app_name
    
    @property
    def app_spec(self) -> algokit_utils.Arc56Contract:
        return self.app_client.app_spec
    
    @property
    def algorand(self) -> _AlgoKitAlgorandClient:
        return self.app_client.algorand

    def clone(
        self,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> "HustleScoreClient":
        return HustleScoreClient(
            self.app_client.clone(
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                approval_source_map=approval_source_map,
                clear_source_map=clear_source_map,
            )
        )

    def new_group(self) -> "HustleScoreComposer":
        return HustleScoreComposer(self)

    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["mint_initial(address)string"],
        return_value: algokit_utils.ABIReturn | None
    ) -> str | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["add_reputation(address,uint64)string"],
        return_value: algokit_utils.ABIReturn | None
    ) -> str | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["get_score(address)uint64"],
        return_value: algokit_utils.ABIReturn | None
    ) -> int | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["get_admin()address"],
        return_value: algokit_utils.ABIReturn | None
    ) -> str | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: typing.Literal["create()string"],
        return_value: algokit_utils.ABIReturn | None
    ) -> str | None: ...
    @typing.overload
    def decode_return_value(
        self,
        method: str,
        return_value: algokit_utils.ABIReturn | None
    ) -> algokit_utils.ABIValue | algokit_utils.ABIStruct | None: ...

    def decode_return_value(
        self,
        method: str,
        return_value: algokit_utils.ABIReturn | None
    ) -> algokit_utils.ABIValue | algokit_utils.ABIStruct | None | int | str:

        if return_value is None:
            return None
    
        arc56_method = self.app_spec.get_arc56_method(method)
        decoded = return_value.get_arc56_value(arc56_method, self.app_spec.structs)
    
        if (arc56_method and
            arc56_method.returns and
            arc56_method.returns.struct and
            isinstance(decoded, dict)):
            struct_class = globals().get(arc56_method.returns.struct)
            if struct_class:
                return struct_class(**typing.cast(dict, decoded))
        return decoded

@dataclasses.dataclass(frozen=True)
class HustleScoreMethodCallCreateParams(
    algokit_utils.AppClientCreateSchema, algokit_utils.BaseAppClientMethodCallParams[
        typing.Any,
        str | None,
    ]
):

    on_complete: typing.Literal[OnComplete.NoOpOC] | None = None
    method: str | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientMethodCallCreateParams:
        method_args = _parse_abi_args(self.args)
        return algokit_utils.AppClientMethodCallCreateParams(
            **{
                **self.__dict__,
                "method": self.method or getattr(self.args, "abi_method_signature", None),
                "args": method_args,
            }
        )

@dataclasses.dataclass(frozen=True)
class HustleScoreBareCallCreateParams(algokit_utils.AppClientBareCallCreateParams):

    on_complete: typing.Literal[OnComplete.DeleteApplicationOC, OnComplete.NoOpOC] | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientBareCallCreateParams:
        return algokit_utils.AppClientBareCallCreateParams(**self.__dict__)

@dataclasses.dataclass(frozen=True)
class HustleScoreBareCallUpdateParams(algokit_utils.AppClientBareCallParams):

    on_complete: typing.Literal[OnComplete.UpdateApplicationOC] | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientBareCallParams:
        return algokit_utils.AppClientBareCallParams(**self.__dict__)

@dataclasses.dataclass(frozen=True)
class HustleScoreBareCallDeleteParams(algokit_utils.AppClientBareCallParams):

    on_complete: typing.Literal[OnComplete.DeleteApplicationOC] | None = None

    def to_algokit_utils_params(self) -> algokit_utils.AppClientBareCallParams:
        return algokit_utils.AppClientBareCallParams(**self.__dict__)

class HustleScoreFactory(algokit_utils.TypedAppFactoryProtocol[HustleScoreMethodCallCreateParams | HustleScoreBareCallCreateParams, HustleScoreBareCallUpdateParams, HustleScoreBareCallDeleteParams]):

    def __init__(
        self,
        algorand: _AlgoKitAlgorandClient,
        *,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        version: str | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
    ):
        self.app_factory = algokit_utils.AppFactory(
            params=algokit_utils.AppFactoryParams(
                algorand=algorand,
                app_spec=APP_SPEC,
                app_name=app_name,
                default_sender=default_sender,
                default_signer=default_signer,
                version=version,
                compilation_params=compilation_params,
            )
        )
        self.params = HustleScoreFactoryParams(self.app_factory)
        self.create_transaction = HustleScoreFactoryCreateTransaction(self.app_factory)
        self.send = HustleScoreFactorySend(self.app_factory)

    @property
    def app_name(self) -> str:
        return self.app_factory.app_name
    
    @property
    def app_spec(self) -> algokit_utils.Arc56Contract:
        return self.app_factory.app_spec
    
    @property
    def algorand(self) -> _AlgoKitAlgorandClient:
        return self.app_factory.algorand

    def deploy(
        self,
        *,
        on_update: algokit_utils.OnUpdate | None = None,
        on_schema_break: algokit_utils.OnSchemaBreak | None = None,
        create_params: HustleScoreMethodCallCreateParams | HustleScoreBareCallCreateParams | None = None,
        update_params: HustleScoreBareCallUpdateParams | None = None,
        delete_params: HustleScoreBareCallDeleteParams | None = None,
        existing_deployments: algokit_utils.ApplicationLookup | None = None,
        ignore_cache: bool = False,
        app_name: str | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
    ) -> tuple[HustleScoreClient, algokit_utils.AppFactoryDeployResult]:

        deploy_response = self.app_factory.deploy(
            on_update=on_update,
            on_schema_break=on_schema_break,
            create_params=create_params.to_algokit_utils_params() if create_params else None,
            update_params=update_params.to_algokit_utils_params() if update_params else None,
            delete_params=delete_params.to_algokit_utils_params() if delete_params else None,
            existing_deployments=existing_deployments,
            ignore_cache=ignore_cache,
            app_name=app_name,
            compilation_params=compilation_params,
            send_params=send_params,
        )

        return HustleScoreClient(deploy_response[0]), deploy_response[1]

    def get_app_client_by_creator_and_name(
        self,
        creator_address: str,
        app_name: str,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        ignore_cache: bool | None = None,
        app_lookup_cache: algokit_utils.ApplicationLookup | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> HustleScoreClient:

        return HustleScoreClient(
            self.app_factory.get_app_client_by_creator_and_name(
                creator_address,
                app_name,
                default_sender,
                default_signer,
                ignore_cache,
                app_lookup_cache,
                approval_source_map,
                clear_source_map,
            )
        )

    def get_app_client_by_id(
        self,
        app_id: int,
        app_name: str | None = None,
        default_sender: str | None = None,
        default_signer: TransactionSigner | None = None,
        approval_source_map: SourceMap | None = None,
        clear_source_map: SourceMap | None = None,
    ) -> HustleScoreClient:

        return HustleScoreClient(
            self.app_factory.get_app_client_by_id(
                app_id,
                app_name,
                default_sender,
                default_signer,
                approval_source_map,
                clear_source_map,
            )
        )

class HustleScoreFactoryParams:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = HustleScoreFactoryCreateParams(app_factory)
        self.update = HustleScoreFactoryUpdateParams(app_factory)
        self.delete = HustleScoreFactoryDeleteParams(app_factory)

class HustleScoreFactoryCreateParams:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
            compilation_params=compilation_params)

    def mint_initial(
        self,
        args: tuple[str] | MintInitialArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "mint_initial(address)string",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

    def add_reputation(
        self,
        args: tuple[str, int] | AddReputationArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "add_reputation(address,uint64)string",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

    def get_score(
        self,
        args: tuple[str] | GetScoreArgs,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "get_score(address)uint64",
                "args": _parse_abi_args(args),
                }
            ),
            compilation_params=compilation_params
        )

    def get_admin(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "get_admin()address",
                "args": None,
                }
            ),
            compilation_params=compilation_params
        )

    def create(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> algokit_utils.AppCreateMethodCallParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.create(
            algokit_utils.AppFactoryCreateMethodCallParams(
                **{
                **dataclasses.asdict(params),
                "method": "create()string",
                "args": None,
                }
            ),
            compilation_params=compilation_params
        )

class HustleScoreFactoryUpdateParams:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        
    ) -> algokit_utils.AppUpdateParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.bare.deploy_update(
            algokit_utils.AppClientBareCallParams(**dataclasses.asdict(params)),
            )

class HustleScoreFactoryDeleteParams:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        
    ) -> algokit_utils.AppDeleteParams:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.params.bare.deploy_delete(
            algokit_utils.AppClientBareCallParams(**dataclasses.asdict(params)),
            )

class HustleScoreFactoryCreateTransaction:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = HustleScoreFactoryCreateTransactionCreate(app_factory)

class HustleScoreFactoryCreateTransactionCreate:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
    ) -> Transaction:

        params = params or algokit_utils.CommonAppCallCreateParams()
        return self.app_factory.create_transaction.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
        )

class HustleScoreFactorySend:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory
        self.create = HustleScoreFactorySendCreate(app_factory)

class HustleScoreFactorySendCreate:

    def __init__(self, app_factory: algokit_utils.AppFactory):
        self.app_factory = app_factory

    def bare(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None,
    ) -> tuple[HustleScoreClient, algokit_utils.SendAppCreateTransactionResult]:

        params = params or algokit_utils.CommonAppCallCreateParams()
        result = self.app_factory.send.bare.create(
            algokit_utils.AppFactoryCreateParams(**dataclasses.asdict(params)),
            send_params=send_params,
            compilation_params=compilation_params
        )
        return HustleScoreClient(result[0]), result[1]

    def create(
        self,
        *,
        params: algokit_utils.CommonAppCallCreateParams | None = None,
        send_params: algokit_utils.SendParams | None = None,
        compilation_params: algokit_utils.AppClientCompilationParams | None = None
    ) -> tuple[HustleScoreClient, algokit_utils.AppFactoryCreateMethodCallResult[str]]:

            params = params or algokit_utils.CommonAppCallCreateParams()
            client, result = self.app_factory.send.create(
                algokit_utils.AppFactoryCreateMethodCallParams(
                    **{
                    **dataclasses.asdict(params),
                    "method": "create()string",
                    "args": None,
                    }
                ),
                send_params=send_params,
                compilation_params=compilation_params
            )
            return_value = None if result.abi_return is None else typing.cast(str, result.abi_return)
    
            return HustleScoreClient(client), algokit_utils.AppFactoryCreateMethodCallResult[str](
                **{
                    **result.__dict__,
                    "app_id": result.app_id,
                    "abi_return": return_value,
                    "transaction": result.transaction,
                    "confirmation": result.confirmation,
                    "group_id": result.group_id,
                    "tx_ids": result.tx_ids,
                    "transactions": result.transactions,
                    "confirmations": result.confirmations,
                    "app_address": result.app_address,
                }
            )

class _HustleScoreUpdateComposer:
    def __init__(self, composer: "HustleScoreComposer"):
        self.composer = composer

class _HustleScoreDeleteComposer:
    def __init__(self, composer: "HustleScoreComposer"):
        self.composer = composer

class HustleScoreComposer:

    def __init__(self, client: "HustleScoreClient"):
        self.client = client
        self._composer = client.algorand.new_group()
        self._result_mappers: list[typing.Callable[[algokit_utils.ABIReturn | None], object] | None] = []

    @property
    def update(self) -> "_HustleScoreUpdateComposer":
        return _HustleScoreUpdateComposer(self)

    @property
    def delete(self) -> "_HustleScoreDeleteComposer":
        return _HustleScoreDeleteComposer(self)

    def mint_initial(
        self,
        args: tuple[str] | MintInitialArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "HustleScoreComposer":
        self._composer.add_app_call_method_call(
            self.client.params.mint_initial(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "mint_initial(address)string", v
            )
        )
        return self

    def add_reputation(
        self,
        args: tuple[str, int] | AddReputationArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "HustleScoreComposer":
        self._composer.add_app_call_method_call(
            self.client.params.add_reputation(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "add_reputation(address,uint64)string", v
            )
        )
        return self

    def get_score(
        self,
        args: tuple[str] | GetScoreArgs,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "HustleScoreComposer":
        self._composer.add_app_call_method_call(
            self.client.params.get_score(
                args=args,
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "get_score(address)uint64", v
            )
        )
        return self

    def get_admin(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "HustleScoreComposer":
        self._composer.add_app_call_method_call(
            self.client.params.get_admin(
                
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "get_admin()address", v
            )
        )
        return self

    def create(
        self,
        params: algokit_utils.CommonAppCallParams | None = None
    ) -> "HustleScoreComposer":
        self._composer.add_app_call_method_call(
            self.client.params.create(
                
                params=params,
            )
        )
        self._result_mappers.append(
            lambda v: self.client.decode_return_value(
                "create()string", v
            )
        )
        return self

    def clear_state(
        self,
        *,
        args: list[bytes] | None = None,
        params: algokit_utils.CommonAppCallParams | None = None,
    ) -> "HustleScoreComposer":
        params=params or algokit_utils.CommonAppCallParams()
        self._composer.add_app_call(
            self.client.params.clear_state(
                algokit_utils.AppClientBareCallParams(
                    **{
                        **dataclasses.asdict(params),
                        "args": args
                    }
                )
            )
        )
        return self
    
    def add_transaction(
        self, txn: Transaction, signer: TransactionSigner | None = None
    ) -> "HustleScoreComposer":
        self._composer.add_transaction(txn, signer)
        return self
    
    def composer(self) -> algokit_utils.TransactionComposer:
        return self._composer
    
    def simulate(
        self,
        allow_more_logs: bool | None = None,
        allow_empty_signatures: bool | None = None,
        allow_unnamed_resources: bool | None = None,
        extra_opcode_budget: int | None = None,
        exec_trace_config: SimulateTraceConfig | None = None,
        simulation_round: int | None = None,
        skip_signatures: bool | None = None,
    ) -> algokit_utils.SendAtomicTransactionComposerResults:
        return self._composer.simulate(
            allow_more_logs=allow_more_logs,
            allow_empty_signatures=allow_empty_signatures,
            allow_unnamed_resources=allow_unnamed_resources,
            extra_opcode_budget=extra_opcode_budget,
            exec_trace_config=exec_trace_config,
            simulation_round=simulation_round,
            skip_signatures=skip_signatures,
        )
    
    def send(
        self,
        send_params: algokit_utils.SendParams | None = None
    ) -> algokit_utils.SendAtomicTransactionComposerResults:
        return self._composer.send(send_params)
