import os
import shutil

# English Data
structure_en = {
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

# Traditional Chinese Data
structure_zh = {
    "subject": {
        "count.txt": ["1個女孩", "2個女孩", "單人", "情侶", "群體"],
        "type.txt": ["人類", "精靈", "仿生人", "動物", "怪物"],
        "role.txt": ["學生", "上班族", "騎士", "法師", "護理師"],
        "age.txt": ["青少年", "成年", "成熟", "小孩", "老年"],
        "ethnicity.txt": ["亞洲人", "白人", "拉丁裔", "非裔", "中東人"],
        "vibe.txt": ["可愛", "酷", "優雅", "帥氣", "陰鬱"]
    },
    "face": {
        "expression.txt": ["微笑", "嚴肅", "想睡", "生氣", "害羞臉紅"],
        "eyes_color.txt": ["棕色眼睛", "藍色眼睛", "綠色眼睛", "紅色眼睛", "異色瞳"],
        "eyes_shape.txt": ["大眼睛", "細長眼", "下垂眼", "吊眼", "垂眼"],
        "makeup.txt": ["淡妝", "濃妝", "紅唇", "眼影", "素顏"],
        "skin.txt": ["白皙皮膚", "小麥色皮膚", "黑皮膚", "蒼白皮膚"],
        "special_marks.txt": ["淚痣", "雀斑", "疤痕", "刺青", "美人痣"],
        "gaze.txt": ["看著觀眾", "看別處", "回頭看", "閉眼"]
    },
    "hair": {
        "color.txt": ["黑髮", "銀髮", "金髮", "粉紅髮", "藍髮"],
        "length.txt": ["短髮", "中長髮", "長髮", "超長髮"],
        "style.txt": ["馬尾", "鮑伯頭", "凌亂髮型", "雙馬尾", "辮子"],
        "details.txt": ["光澤髮質", "髮飾", "髮帶", "呆毛"]
    },
    "body": {
        "height.txt": ["高挑", "嬌小", "平均身高"],
        "build.txt": ["纖細", "曲線", "肌肉", "肉感", "骨感"],
        "posture.txt": ["放鬆姿勢", "優雅姿勢", "動態姿勢", "駝背"],
        "hands.txt": ["手插口袋", "拿著手機", "比YA", "雙手交叉"]
    },
    "outfit": {
        "theme": {
            "casual.txt": ["帽T", "牛仔褲", "T恤", "短褲"],
            "school.txt": ["學校制服", "水手服", "西裝外套", "水手服(serafuku)"],
            "business.txt": ["西裝", "西裝外套", "鉛筆裙", "領帶"],
            "dress.txt": ["長洋裝", "雞尾酒禮服", "夏季洋裝", "禮服"],
            "sporty.txt": ["運動服", "田徑服", "健身服", "瑜珈褲"],
            "traditional.txt": ["和服", "漢服", "旗袍", "浴衣"]
        },
        "top.txt": ["襯衫", "T恤", "夾克", "毛衣", "背心"],
        "bottom.txt": ["裙子", "短褲", "長褲", "百褶裙", "內搭褲"],
        "onepiece.txt": ["洋裝", "大衣式洋裝", "女僕裝", "護士服"],
        "shoes.txt": ["運動鞋", "靴子", "高跟鞋", "涼鞋", "樂福鞋"],
        "accessories.txt": ["眼鏡", "耳環", "項鍊", "帽子", "面具"],
        "color_palette.txt": ["單色系", "粉色系", "鮮豔色系", "暗色系"],
        "material.txt": ["皮革", "丹寧", "絲綢", "乳膠", "棉質"]
    },
    "pose": {
        "base.txt": ["站立", "坐著", "躺著", "跪著", "蹲著"],
        "action.txt": ["走路", "跑步", "跳舞", "戰鬥", "跳躍"],
        "hand_pose.txt": ["揮手", "比YA", "指著", "伸手"],
        "interaction.txt": ["拿著咖啡", "使用筆電", "看書", "吃東西"],
        "dynamic.txt": ["頭髮飄動", "動態模糊", "風", "漂浮"]
    },
    "scene": {
        "location": {
            "indoor.txt": ["咖啡廳", "辦公室", "教室", "臥室", "圖書館"],
            "outdoor.txt": ["街道", "公園", "海灘", "森林", "城市景觀"]
        },
        "time.txt": ["早上", "日落", "夜晚", "中午", "黃昏"],
        "weather.txt": ["晴天", "雨天", "雪", "多雲", "暴風雨"],
        "season.txt": ["春天", "秋天", "夏天", "冬天"],
        "background_detail.txt": ["散景背景", "繁忙街道", "雜亂房間", "極簡"],
        "props.txt": ["霓虹燈", "書架", "花", "家具"]
    },
    "camera": {
        "shot_type.txt": ["特寫", "半身", "全身", "肖像", "七分身(cowboy shot)"],
        "angle.txt": ["低角度", "高角度", "荷蘭式鏡頭", "正面平視"],
        "lens.txt": ["35mm", "50mm", "廣角", "長焦", "魚眼"],
        "composition.txt": ["居中", "三分法", "對稱", "黃金比例"],
        "depth_of_field.txt": ["淺景深", "散景", "深焦"]
    },
    "lighting": {
        "source.txt": ["自然光", "輪廓光", "攝影棚光", "陽光"],
        "mood.txt": ["電影光", "柔光", "戲劇性光線", "陰暗氛圍"],
        "color_temp.txt": ["暖光", "冷光", "中性光"],
        "contrast.txt": ["高對比", "柔和對比", "低調(Low key)", "高調(High key)"]
    },
    "style": {
        "medium.txt": ["照片", "水彩", "油畫", "數位藝術", "素描"],
        "genre.txt": ["賽博龐克", "奇幻", "生活片段(Slice of life)", "科幻", "恐怖"],
        "render.txt": ["超精細", "高品質", "8k", "照片級真實"],
        "art_direction.txt": ["電影感", "極簡主義", "超現實", "抽象"],
        "quality_tags.txt": ["傑作(masterpiece)", "最佳品質(best quality)", "超高解析度(absurdres)", "難以置信的細節"]
    },
    "negative": {
        "general.txt": ["低解析度", "模糊", "解剖結構錯誤", "品質差"],
        "hands.txt": ["手部崩壞", "多餘手指", "手指缺失"],
        "face.txt": ["臉部變形", "鬥雞眼", "醜"],
        "artifacts.txt": ["jpeg壓縮瑕疵", "浮水印", "簽名", "使用者名稱"]
    },
    "control": {
        "fixed_identity.txt": ["", "演員: 安海瑟薇", "角色: 初音未來"],
        "forbidden_mix.txt": ["裸體", "nsfw"],
        "prompt_syntax.txt": ["(masterpiece:1.2)", "[red hair]"]
    }
}

def create_structure(base, data):
    if os.path.exists(base):
        try:
            shutil.rmtree(base)
        except:
            pass
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

create_structure("wildcards_en", structure_en)
create_structure("wildcards_zh", structure_zh)

# Cleanup old folder if exists
if os.path.exists("wildcards"):
    shutil.rmtree("wildcards")

print("Multi-language wildcards structure created successfully.")
