from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io


def create_background_pdf(color_hex):
    """Creates a temporary one-page PDF with a solid background color."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFillColor(color_hex)
    can.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def create_split_pages_with_bg(input_file, output_file, bg_color="#FEFAF2"):
    reader = PdfReader(input_file)
    writer = PdfWriter()

    A4_W = 595.28
    A4_H = 841.89
    HALF_H = A4_H / 2

    for i in range(min(2, len(reader.pages))):
        source_page = reader.pages[i]

        # Measure and clean source
        in_h = float(source_page.cropbox.height)
        source_page.transfer_rotation_to_content()
        source_page.rotation = 0

        # 1. Create a fresh A4 page with the background color
        new_page = create_background_pdf(bg_color)

        # 2. Calculate Scale to fill the width
        scale = A4_W / in_h

        # 3. Positioning logic
        ty_offset = HALF_H if i == 0 else 0
        tx_correction = in_h * scale

        trans = Transformation() \
            .rotate(90) \
            .scale(sx=scale, sy=scale) \
            .translate(tx=tx_correction, ty=ty_offset)

        # 4. Merge source page OVER the background
        new_page.merge_transformed_page(source_page, trans)
        writer.add_page(new_page)

    with open(output_file, "wb") as f:
        writer.write(f)


# Change "#F5F5DC" to any hex color you like (e.g., "#FFFFFF" for pure white)
create_split_pages_with_bg("Barbara.pdf", "okladka.pdf", bg_color="#F5F5DC")
