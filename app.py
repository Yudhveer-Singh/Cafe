# Copyright (C) 2026 Yudhveer Singh (https://github.com/yudhveer-singh/)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See <https://www.gnu.org/licenses/> for details.

import gradio as gr
import uvicorn
from fastapi import FastAPI

from home import app as home_app # ready
from aadhaar import app as aadhaar_app # ready
from pic import app as pic_app, CSS # ready
from pan import app as pan_app # ready
from ayushman import app as ayushman_app # ready
from ayushman_5lakh import app as ayushman_5lakh_app # ready
from voter import app as voter_app # ready
from uan import app as uan_app # ready
from rich import print as printf

cat = """
            ╱|、
          (˚ˎ 。7
          |、˜〵        
          じしˍ,)ノ
"""

app = FastAPI()

app = gr.mount_gradio_app(app, home_app, path="/home")
app = gr.mount_gradio_app(app, aadhaar_app, path="/aadhaar")
app = gr.mount_gradio_app(app, pic_app, path="/pic", css = CSS)
app = gr.mount_gradio_app(app, pan_app, path="/pan")
app = gr.mount_gradio_app(app, uan_app, path="/uan")
app = gr.mount_gradio_app(app, ayushman_app, path="/ayushman")
app = gr.mount_gradio_app(app, ayushman_5lakh_app, path="/ayushman_5lakh")
app = gr.mount_gradio_app(app, voter_app, path="/voter")

if __name__ == "__main__":
    printf(f"[cyan bold]{cat}[/]")
    uvicorn.run(app, host="0.0.0.0", port=7860)
