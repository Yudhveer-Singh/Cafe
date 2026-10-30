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
md = """
# Pages
- [Home Page].(http://127.0.0.1:7860/home ).✅
- [Aadhaar Card].(http://127.0.0.1:7860/aadhaar ).✅
- [Pics].(http://127.0.0.1:7860/pic ).✅
- [Pan].(http://127.0.0.1:7860/pan ).✅
- [ayushman].(http://127.0.0.1:7860/ayushman ).⏳
- [uan].(http://127.0.0.1:7860/uan ).⏳
- [ayushman 5L].(http://127.0.0.1:7860/ayushman_5lakh ).✅
- [voter].(http://127.0.0.1:7860/voter ).✅
"""

with gr.Blocks(title="Home Page") as app:
	gr.Markdown(md)

if __name__ == "__main_":
	app.launch()
