import requests

def fetch_openverse_image(query):
    """Fetch a single CC0 image URL from Openverse for a given word."""
    url = f"https://api.openverse.engineering/v1/images?q={query}&license=cc0&page_size=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            return data['results'][0]['url']
    except Exception as e:
        print(f"Error fetching image for '{query}':", e)
    return None

def generate_html(words, image_urls, output_file='presentation.html'):
    slides = []
    slide_id = 1

    for word, img in zip(words, image_urls):
        # Title Slide
        slides.append(f'''
        <div class="slide" id="slide-{slide_id}">
            <h1>{word}</h1>
        </div>''')
        slide_id += 1
        # Image Slide
        if img:
            slides.append(f'''
            <div class="slide" id="slide-{slide_id}">
                <img src="{img}" alt="{word}">
            </div>''')
        else:
            slides.append(f'''
            <div class="slide" id="slide-{slide_id}">
                <h2>No image found for "{word}"</h2>
            </div>''')
        slide_id += 1

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Openverse Presentation</title>
    <style>
        body {{
            margin: 0;
            background: #111;
            color: white;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .slide {{
            display: none;
            width: 100%;
            height: 100%;
            text-align: center;
        }}
        .active {{
            display: block;
        }}
        img {{
            max-width: 90%;
            max-height: 90%;
        }}
        h1 {{
            font-size: 4em;
        }}
        h2 {{
            font-size: 2em;
        }}
    </style>
</head>
<body>

{''.join(slides)}

<script>
    let current = 1;
    const slides = document.querySelectorAll('.slide');
    const total = slides.length;

    function showSlide(n) {{
        slides.forEach(s => s.classList.remove('active'));
        document.getElementById('slide-' + n).classList.add('active');
    }}

    document.addEventListener('keydown', e => {{
        if (e.key === 'ArrowRight' || e.key === ' ') {{
            if (current < total) {{
                current++;
                showSlide(current);
            }}
        }} else if (e.key === 'ArrowLeft') {{
            if (current > 1) {{
                current--;
                showSlide(current);
            }}
        }}
    }});

    document.addEventListener('click', () => {{
        current = (current % total) + 1;
        showSlide(current);
    }});

    showSlide(current);
</script>

</body>
</html>
"""
    with open(output_file, 'w') as f:
        f.write(html_template)
    print(f"Presentation saved to {output_file}")

# --- Example Usage ---
if __name__ == "__main__":
    words = ["tree", "ocean", "moon", "desert", "bird", "city", "snow", "cloud", "fire", "mountain"]
    print("Fetching images...")
    image_urls = [fetch_openverse_image(word) for word in words]
    generate_html(words, image_urls)
