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

import pymupdf as fitz  # PyMuPDF

A4_WIDTH = 595.28
A4_HEIGHT = 841.89


def images_to_pdf(
    images,
    images_per_row=5,
    margin_x=20, # 50 on site; me = 20
    margin_y=36, # 36 on site; me = 20
    gap_x=8, # 10 on site:idcard.store; me = 6
    gap_y=8, # my init = 6
    image_width=99, # 93 on site:idcard; real = 99
    image_height=128, #124 on site; real = 128
    cut_lines=True,
    keep_proportion = True
):
    """Arrange images on A4 pages, centered horizontally."""

    if not images:
        raise ValueError("No images supplied")

    if images_per_row < 1:
        raise ValueError("images_per_row must be >= 1")

    # Width of the complete row/grid
    grid_width = (
        images_per_row * image_width
        + (images_per_row - 1) * gap_x
    )

    if grid_width > A4_WIDTH - 2 * margin_x:
        raise ValueError("Images do not fit horizontally on A4")

    # Number of rows that fit vertically
    usable_height = A4_HEIGHT - 2 * margin_y

    rows_per_page = int(
        (usable_height + gap_y)
        / (image_height + gap_y)
    )

    if rows_per_page < 1:
        raise ValueError("Images are too tall to fit on A4")

    images_per_page = images_per_row * rows_per_page

    # ---------------------------------------------------------
    # Center horizontally
    # ---------------------------------------------------------

    start_x = (A4_WIDTH - grid_width) / 2

    doc = fitz.open()

    # ---------------------------------------------------------
    # Create pages
    # ---------------------------------------------------------

    for page_start in range(0, len(images), images_per_page):

        page_images = images[
            page_start:page_start + images_per_page
        ]

        page = doc.new_page(
            width=A4_WIDTH,
            height=A4_HEIGHT,
        )

        # Vertically starts at margin_y
        start_y = margin_y

        for i, image in enumerate(page_images):

            row = i // images_per_row
            col = i % images_per_row

            x = start_x + col * (image_width + gap_x)
            y = start_y + row * (image_height + gap_y)

            rect = fitz.Rect(
                x,
                y,
                x + image_width,
                y + image_height,
            )

            page.insert_image(
                rect,
                filename=image,
                keep_proportion = keep_proportion
            )

            if cut_lines:
                page.draw_rect(
                    rect,
                    color=(0, 0, 0),
                    width=0.2,
                )

    return doc

def cards_to_pdf(
    images,
    images_per_row=5,
    margin_x=20,
    margin_y=20,
    gap_x=6,
    gap_y=6,
    image_width=99,
    image_height=128,
    cut_lines=True,
    keep_proportion = True
):
	return images_to_pdf(
	    images,
	    images_per_row=5,
	    margin_x=20,
	    margin_y=20,
	    gap_x=6,
	    gap_y=6,
	    image_width=99,
	    image_height=128,
	    cut_lines=True,
	    keep_proportion = True
	)

def main():

    images = [
        "hum.jpeg"
    ]*59

    doc = images_to_pdf(
        images,
        images_per_row=5,

        margin_x=2,
        margin_y=32,

        gap_x=6,
        gap_y=6,

        image_width= 77, #85, #100, real 99
        image_height= 100, #114, #133.33, real 128

        cut_lines=True,
    )

    doc.save("passport_photos.pdf")
    doc.close()


if __name__ == "__main__":
    main()