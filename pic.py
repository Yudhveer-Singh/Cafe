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

import gradio as gr
import pymupdf as fitz

from image_parser import images_to_pdf


def create_pdf(images, *copy_counts):
    if not images:
        raise gr.Error("Please upload at least one image.")

    expanded_images = []

    for image, count in zip(images, copy_counts):
        count = int(count or 0)

        if not 1 <= count <= 100:
            raise gr.Error("Copies must be between 1 and 100.")

        expanded_images.extend([image] * count)

    pdf = images_to_pdf(
    	expanded_images,
    	keep_proportion = False
    )

    if isinstance(pdf, fitz.Document):
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", delete=False
        ) as f:
            output_path = f.name

        try:
            pdf.save(output_path)
        finally:
            pdf.close()

        return output_path

    return str(pdf)


def change_count(value, step):
    return max(1, min(100, int(value or 5) + step))


CSS = """
.copy-control {
    gap: 4px !important;
    align-items: center !important;
}

.copy-control button {
    min-width: 34px !important;
    width: 34px !important;
    height: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    font-size: 18px !important;
}

.copy-control input {
    text-align: center !important;
    font-weight: 600 !important;
}

.image-card {
    border: 1px solid var(--border-color-primary);
    border-radius: 12px;
    padding: 10px;
}

#generate-btn {
    position: relative;
    width: 100%;
    margin-top: 20px;
}
"""


with gr.Blocks(title="Image to A4 PDF") as app:
    gr.Markdown("# Image to PDF")
    gr.Markdown("Upload photos and configure print quantities.")

    images = gr.File(
        label="Upload Images",
        file_count="multiple",
        file_types=["image"],
        type="filepath",
    )

    with gr.Column():
        @gr.render(inputs=images)
        def render_copy_inputs(uploaded_images):
            if not uploaded_images:
                gr.Markdown("Upload images to get started.")
                return

            counts = []

            for i, image in enumerate(uploaded_images):
                filename = os.path.basename(image)

                with gr.Row(elem_classes=["image-card"]):
                    gr.Image(
                        value=image,
                        label=None,
                        show_label=False,
                        interactive=False,
                        height=120, #120
                        width=140, #140
                        container=False,
                    )

                    with gr.Column():
                        gr.Markdown(
                            f"**{i + 1}. {filename}**"
                        )

                        with gr.Row(elem_classes=["copy-control"]):
                            minus = gr.Button(
                                "−",
                                size="sm",
                                min_width=34,
                            )

                            count = gr.Number(
                                value=5,
                                show_label=False,
                                precision=0,
                                minimum=1,
                                maximum=100,
                                interactive=False,
                                key=f"copies_{i}_{filename}",
                                preserved_by_key=["value"],
                                container=False,
                            )

                            plus = gr.Button(
                                "+",
                                size="sm",
                                min_width=34,
                            )

                        minus.click(
                            fn=lambda v: change_count(v, -1),
                            inputs=count,
                            outputs=count,
                        )

                        plus.click(
                            fn=lambda v: change_count(v, 1),
                            inputs=count,
                            outputs=count,
                        )

                        counts.append(count)

            generate.click(
                fn=create_pdf,
                inputs=[images] + counts,
                outputs=output,
            )

    generate = gr.Button(
        "Generate PDF",
        variant="primary",
        elem_id="generate-btn",
    )

    output = gr.File(label="Download PDF")


if __name__ == "__main__":
    app.launch(css = CSS)
    #app.launch(share=True)