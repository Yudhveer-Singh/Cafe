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

import secrets
import gradio as gr
import pymupdf as fitz  # PyMuPDF
from typing import List
import tempfile
import os
from image_parser import images_to_pdf

def process_pdfs(pdf_files):
    """
    Process multiple PDFs: extract front and back pages, combine into one PDF
    
    Args:
        pdf_files: List of PDF file paths from Gradio
    
    Returns:
        str: Path to the combined PDF file
    """
    
    # Coordinates for extraction (modify these as needed)
    FRONT = (104, 644, 411, 800)
    PAGE_FRONT = 0
    BACK = (444, 645, 751, 801)  # Replace with actual back coordinates
    PAGE_BACK = 0
    
    image_paths = []
    temp_dir = tempfile.mkdtemp()
    image_counter = 0
    
    try:
        # Process each PDF file
        for pdf_file in pdf_files:
            # Open PDF from file path
            pdf_doc = fitz.open(pdf_file)
            
            # Extract front page image
            front_page = pdf_doc[PAGE_FRONT]
            front_image = front_page.get_pixmap(
                matrix=fitz.Matrix(4,4),
                clip=fitz.Rect(FRONT),
                alpha=False,
            )
            front_path = os.path.join(temp_dir, f"image_{image_counter}.png")
            front_image.save(front_path)
            image_paths.append(front_path)
            image_counter += 1
            
            # Extract back page image
            if PAGE_BACK < len(pdf_doc):  # Safety check
                back_page = pdf_doc[PAGE_BACK]
                back_image = back_page.get_pixmap(
                    matrix=fitz.Matrix(4,4),
                    clip=fitz.Rect(BACK),
                    alpha=False,
                )
                back_path = os.path.join(temp_dir, f"image_{image_counter}.png")
                back_image.save(back_path)
                image_paths.append(back_path)
                image_counter += 1
            
            pdf_doc.close()
        
        # Pass image file paths to images_to_pdf function
        combined_doc = images_to_pdf(
        	images = image_paths,
        	images_per_row=2,
            margin_x=20,
            margin_y=20, #16 site:idcard
            gap_x=6,
            gap_y=6,
            image_width=240 - 5, #245
            image_height=150 - 3, #152
            cut_lines=True,
            keep_proportion=True,
        )
        
        # Save combined PDF to temporary file
        output_pdf_path = os.path.join(temp_dir, f"tmp_ayush_{secrets.token_urlsafe(6)}.pdf")
        combined_doc.save(output_pdf_path)
        combined_doc.close()
        
        return output_pdf_path
    
    except Exception as e:
        # Cleanup on error
        for img_path in image_paths:
            if os.path.exists(img_path):
                os.remove(img_path)
        raise e

tit = "Ayushman Card Printer"
# Create Gradio interface
with gr.Blocks(title=tit) as app:
    gr.Markdown(f"# {tit}")
    gr.Markdown("You can upload multiple PDFs.")
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(
                label="Upload PDFs",
                file_count="multiple",
                file_types=[".pdf"]
            )
            process_btn = gr.Button("Process PDFs", variant="primary")
        
        with gr.Column():
            pdf_output = gr.File(label="Download Printable PDF", type="binary")
    
    # Connect button to processing function
    process_btn.click(
        fn=process_pdfs,
        inputs=[pdf_input],
        outputs=[pdf_output]
    )


if __name__ == "__main__":
    app.launch()
