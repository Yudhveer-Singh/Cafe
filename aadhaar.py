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

import os
import tempfile
import secrets
import gradio as gr
import pymupdf as fitz  # PyMuPDF

from image_parser import images_to_pdf


# --------------------------------------------------
# CONFIGURATION: ADJUST THESE PDF COORDINATES
# --------------------------------------------------

# Page number is zero-based.
PAGE_NUMBER = 0

# Rectangle coordinates: (x0, y0, x1, y1)
# Replace these dummy coordinates with the actual
# positions of the front and backside of your Aadhaar.
FRONT_RECT = (49, 574, 300, 733)
BACK_RECT = (312, 575, 563, 733)


def create_aadhaar_pdf(pdf_file, password):
    if pdf_file is None:
        raise gr.Error("Please upload a PDF.")

    password = password or ""

    doc = None

    try:
        # Open the uploaded PDF.
        doc = fitz.open(pdf_file)

        # Unlock the PDF if password-protected.
        if doc.needs_pass:
            if not password:
                raise gr.Error("This PDF requires a password.")

            if not doc.authenticate(password):
                raise gr.Error("Incorrect PDF password.")

        if doc.page_count == 0:
            raise gr.Error("The PDF contains no pages.")

        if PAGE_NUMBER >= doc.page_count:
            raise gr.Error(
                f"Page {PAGE_NUMBER + 1} does not exist. "
                f"The PDF has {doc.page_count} pages."
            )

        page = doc[PAGE_NUMBER]

        # Ensure both crop rectangles are inside the page.
        page_rect = page.rect

        front_rect = fitz.Rect(FRONT_RECT)
        back_rect = fitz.Rect(BACK_RECT)

        if not page_rect.contains(front_rect):
            raise gr.Error(
                "FRONT_RECT is outside the PDF page. "
                "Correct its coordinates in aadhaar.py."
            )

        if not page_rect.contains(back_rect):
            raise gr.Error(
                "BACK_RECT is outside the PDF page. "
                "Correct its coordinates in aadhaar.py."
            )

        # Render each rectangle as a PNG image.
        # Higher resolution gives better print quality.
        zoom = 4

        front_pix = page.get_pixmap(
            matrix=fitz.Matrix(zoom, zoom),
            clip=front_rect,
            alpha=False,
        )

        back_pix = page.get_pixmap(
            matrix=fitz.Matrix(zoom, zoom),
            clip=back_rect,
            alpha=False,
        )

        # Save temporary image files.
        # images_to_pdf() receives a list of image paths.
        with tempfile.TemporaryDirectory() as temp_dir:
            front_path = os.path.join(temp_dir, "aadhaar_front.png")
            back_path = os.path.join(temp_dir, "aadhaar_back.png")

            front_pix.save(front_path)
            back_pix.save(back_path)

            images = [front_path, back_path]

            # Generate the printable PDF using your function.
            output_doc = images_to_pdf(
                images=images,
                images_per_row=2,
                margin_x=20,
                margin_y=20, #16 site:idcard
                gap_x=6,
                gap_y=6,
                image_width=240 - 5, #245
                image_height=150 - 3, #152
                cut_lines=True,
                keep_proportion=False,
            )

            # Save the generated PDF before temporary images
            # are deleted.
            output_path = os.path.join(
                tempfile.gettempdir(),
                f"tmp_aadhaar_{secrets.token_urlsafe(6)}.pdf",
            )

            output_doc.save(output_path)
            output_doc.close()

        return output_path

    except gr.Error:
        raise

    except Exception as exc:
        raise gr.Error(f"Failed to process PDF: {exc}") from exc

    finally:
        if doc is not None:
            doc.close()


# --------------------------------------------------
# GRADIO INTERFACE
# --------------------------------------------------

with gr.Blocks(title="Aadhaar PDF Printer") as app:
    gr.Markdown("# Aadhaar PDF Printer")
    gr.Markdown(
        "Upload a PDF containing your Aadhaar card. "
        "The app extracts the front and backside and "
        "generates a printable PDF."
    )

    with gr.Row():
        pdf_input = gr.File(
            label="Upload PDF",
            file_types=[".pdf"],
            type="filepath",
        )

        password_input = gr.Textbox(
            label="PDF Password",
            placeholder="Enter password if required",
            type="text", # "password",
        )

    generate_button = gr.Button(
        "Generate Printable PDF",
        variant="primary",
    )

    output_pdf = gr.File(
        label="Download Printable PDF",
    )

    generate_button.click(
        fn=create_aadhaar_pdf,
        inputs=[pdf_input, password_input],
        outputs=output_pdf,
    )


if __name__ == "__main__":
    app.launch()
