import os

structure = {
    "subject": {
        "count.txt": ["1girl", "2girls", "solo", "couple", "group"],
        "type.txt": ["human", "elf", "android", "animal", "monster"],
        "role.txt": ["student", "office_worker", "knight", "mage", "nurse"],
        "age.txt": ["teen", "adult", "mature", "child", "elderly"],
        "ethnicity.txt": ["asian", "caucasian", "latinx", "african", "middle_eastern"],
        "vibe.txt": ["cute", "cool", "elegant", "badass", "gloomy"]
    },
    "face": {
        "expression.txt": ["smile", "serious", "sleepy", "angry", "blush"],
        "eyes_color.txt": ["brown eyes", "blue eyes", "green eyes", "red eyes", "heterochromia"],
        "eyes_shape.txt": ["big eyes", "narrow eyes", "droopy eyes", "tsurime", "tareme"],
        "makeup.txt": ["natural makeup", "heavy makeup", "red lipstick", "eyeshadow", "no makeup"],
        "skin.txt": ["fair skin", "tan skin", "dark skin", "pale skin"],
        "special_marks.txt": ["mole under eye", "freckles", "scar", "tattoo", "beauty mark"],
        "gaze.txt": ["looking at viewer", "looking away", "looking back", "closed eyes"]
    },
    "hair": {
        "color.txt": ["black hair", "silver hair", "blonde hair", "pink hair", "blue hair"],
        "length.txt": ["short hair", "medium hair", "long hair", "very long hair"],
        "style.txt": ["ponytail", "bob cut", "messy", "twintails", "braid"],
        "details.txt": ["shiny hair", "hair ornament", "hair ribbon", "ahoge"]
    },
    "body": {
        "height.txt": ["tall", "petite", "average height"],
        "build.txt": ["slim", "curvy", "muscular", "chubby", "skinny"],
        "posture.txt": ["relaxed posture", "elegant posture", "dynamic posture", "slouching"],
        "hands.txt": ["hands in pockets", "holding phone", "peace sign", "crossed arms"]
    },
    "outfit": {
        "theme": {
            "casual.txt": ["hoodie", "jeans", "t-shirt", "shorts"],
            "school.txt": ["school uniform", "sailor uniform", "blazer", "serafuku"],
            "business.txt": ["suit", "blazer", "pencil skirt", "tie"],
            "dress.txt": ["long dress", "cocktail dress", "summer dress", "gown"],
            "sporty.txt": ["sportswear", "tracksuit", "gym clothes", "yoga pants"],
            "traditional.txt": ["kimono", "hanfu", "cheongsam", "yukata"]
        },
        "top.txt": ["blouse", "t-shirt", "jacket", "sweater", "tank top"],
        "bottom.txt": ["skirt", "shorts", "pants", "pleated skirt", "leggings"],
        "onepiece.txt": ["dress", "coat dress", "maid", "nurse uniform"],
        "shoes.txt": ["sneakers", "boots", "heels", "sandals", "loafers"],
        "accessories.txt": ["glasses", "earrings", "necklace", "hat", "mask"],
        "color_palette.txt": ["monochrome", "pastel colors", "vivid colors", "dark theme"],
        "material.txt": ["leather", "denim", "silk", "latex", "cotton"]
    },
    "pose": {
        "base.txt": ["standing", "sitting", "lying", "kneeling", "squatting"],
        "action.txt": ["walking", "running", "dancing", "fighting", "jumping"],
        "hand_pose.txt": ["waving", "peace sign", "pointing", "reaching"],
        "interaction.txt": ["holding coffee", "using laptop", "reading book", "eating"],
        "dynamic.txt": ["hair flowing", "motion blur", "wind", "floating"]
    },
    "scene": {
        "location": {
            "indoor.txt": ["café", "office", "classroom", "bedroom", "library"],
            "outdoor.txt": ["street", "park", "beach", "forest", "cityscape"]
        },
        "time.txt": ["morning", "sunset", "night", "noon", "dusk"],
        "weather.txt": ["sunny", "rainy", "snow", "cloudy", "storm"],
        "season.txt": ["spring", "autumn", "summer", "winter"],
        "background_detail.txt": ["bokeh background", "busy street", "cluttered room", "minimalist"],
        "props.txt": ["neon signs", "bookshelves", "flowers", "furniture"]
    },
    "camera": {
        "shot_type.txt": ["close-up", "half body", "full body", "portrait", "cowboy shot"],
        "angle.txt": ["low angle", "high angle", "dutch angle", "straight on"],
        "lens.txt": ["35mm", "50mm", "wide angle", "telephoto", "fisheye"],
        "composition.txt": ["centered", "rule of thirds", "symmetry", "golden ratio"],
        "depth_of_field.txt": ["shallow DOF", "bokeh", "deep focus"]
    },
    "lighting": {
        "source.txt": ["natural light", "rim light", "studio light", "sunlight"],
        "mood.txt": ["cinematic lighting", "soft light", "dramatic lighting", "dark and moody"],
        "color_temp.txt": ["warm lighting", "cool lighting", "neutral lighting"],
        "contrast.txt": ["high contrast", "soft contrast", "low key", "high key"]
    },
    "style": {
        "medium.txt": ["photo", "watercolor", "oil painting", "digital art", "sketch"],
        "genre.txt": ["cyberpunk", "fantasy", "slice of life", "sci-fi", "horror"],
        "render.txt": ["ultra detailed", "high quality", "8k", "photorealistic"],
        "art_direction.txt": ["cinematic", "minimalistic", "surreal", "abstract"],
        "quality_tags.txt": ["masterpiece", "best quality", "absurdres", "incredibly detailed"]
    },
    "negative": {
        "general.txt": ["lowres", "blurry", "bad anatomy", "bad quality"],
        "hands.txt": ["bad hands", "extra fingers", "missing fingers"],
        "face.txt": ["deformed face", "cross-eye", "ugly"],
        "artifacts.txt": ["jpeg artifacts", "watermark", "signature", "username"]
    },
    "control": {
        "fixed_identity.txt": ["", "actor: anne hathaway", "character: hatsune miku"],
        "forbidden_mix.txt": ["nude", "nsfw"],
        "prompt_syntax.txt": ["(masterpiece:1.2)", "[red hair]"]
    }
}

base_dir = "wildcards"

def create_structure(base, data):
    if not os.path.exists(base):
        os.makedirs(base)
    
    for key, value in data.items():
        path = os.path.join(base, key)
        if isinstance(value, dict):
            # It's a directory
            create_structure(path, value)
        elif isinstance(value, list):
            # It's a file
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(value))

create_structure(base_dir, structure)
print("Wildcards structure created successfully.")
