# reddit_card.py
from PIL import Image, ImageDraw, ImageFont
import os

def create_reddit_card(title,
                       subreddit="r/confession",
                       upvotes="20K+",
                       comments="100+",
                       template_path="reddit_card/template.png",
                       output_path="reddit_card/card.png",
                       title_position=(60, 180),  # ✅ Lower position for better centering
                       max_width=960,
                       font_size=44):  # ✅ Larger font for Mode 1&2
    """
    Create a Reddit card overlay using your pre-made template.
    Used for Mode 1 & 2 (Full Pipeline)
    """
    if not os.path.exists(template_path):
        print(f"⚠️  Template not found: {template_path}")
        return None
    
    # Open template
    template = Image.open(template_path).convert('RGBA')
    
    # ✅ KEEP ORIGINAL SIZE 1080x500 for Mode 1&2
    template = template.resize((1080, 500), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(template)
    
    # Load font
    try:
        font_regular = ImageFont.truetype("arial.ttf", font_size)
        font_medium = ImageFont.truetype("arial.ttf", font_size)
    except:
        font_regular = ImageFont.load_default()
        font_medium = font_regular
    
    # ✅ NO CHARACTER LIMIT - Show full title
    title_text = title
    
    # Text wrapping function
    def wrap_text(text, font, max_width, draw):
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines
    
    # Wrap title text
    wrapped_lines = wrap_text(title_text, font_regular, max_width, draw)
    
    # Draw title text
    text_x, text_y = title_position
    line_height = font_size + 10  # Line spacing
    
    print(f"📝 Drawing {len(wrapped_lines)} line(s) of text...")
    # ✅ SHOW ALL LINES (no max limit)
    for i, line in enumerate(wrapped_lines):
        current_y = text_y + (i * line_height)
        # Draw text with subtle shadow
        draw.text((text_x + 1, current_y + 1), line, font=font_medium, fill=(0, 0, 0, 128))
        draw.text((text_x, current_y), line, font=font_medium, fill=(0, 0, 0, 255))
        print(f"   Line {i+1}: '{line}'")
    
    # Save the card
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    template.save(output_path, 'PNG')
    print(f"✅ Reddit card saved to: {output_path}")
    print(f"   Size: {template.size}")
    print(f"   Title lines: {len(wrapped_lines)}")
    return output_path