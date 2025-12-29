import os
import shutil

# English Data
structure_en = {
    "subject": {
        "count.txt": ["1girl", "2girls", "solo focus", "couple together", "group of friends"],
        "type.txt": ["human female", "mystical elf", "cybernetic android", "anthropomorphic animal", "fantasy monster girl"],
        "role.txt": ["diligent student", "busy office worker", "armored knight", "arcane mage", "caring nurse"],
        "age.txt": ["energetic teen", "young adult", "mature woman", "small child", "wise elderly"],
        "ethnicity.txt": ["East Asian descent", "Caucasian descent", "Latin American descent", "African descent", "Middle Eastern descent"],
        "vibe.txt": ["cute and adorable vibe", "cool and stylish vibe", "elegant and sophisticated vibe", "badass and tough vibe", "gloomy and mysterious vibe", "cheerful and sunny vibe", "mysterious and enigmatic vibe", "melancholy and sad vibe", "energetic and sporty vibe"],
        "clothing_style.txt": ["vintage 1920s flapper style", "high-tech cyberpunk techwear", "victorian steampunk aesthetic", "boho-chic festival look", "urban modern streetwear", "avant-garde high-fashion", "dark gothic lolita style", "comfortable athleisure wear", "clean preppy academy style", "90s grunge aesthetic", "minimalist modern style"],
        "fabric.txt": ["smooth silk", "plush velvet", "textured denim", "shiny leather", "glossy latex", "delicate lace", "sparkling sequined fabric", "chunky knitted yarn", "rough canvas", "smooth satin", "breathable linen", "sheer translucent fabric"]
    },
    "face": {
        "expression.txt": ["warm and gentle smile", "serious and focused expression", "yawning, sleepy face", "frowning in anger", "shyly blushing", "laughing heartily", "tears streaming down face", "wide-eyed surprise", "confused tilt of head", "terrified expression", "seductive gaze", "disgusted sneer", "emotionless poker face", "beaming with joy", "eyes welling up with tears", "furious rage"],
        "eyes_color.txt": ["deep brown eyes", "piercing blue eyes", "emerald green eyes", "ruby red eyes", "heterochromia iridum (one blue, one green)"],
        "eyes_shape.txt": ["large innocent eyes", "sharp narrow eyes", "sleepy droopy eyes", "sharp tsurime eyes", "gentle tareme eyes"],
        "makeup.txt": ["subtle natural makeup", "heavy gothic makeup", "bold red lipstick", "shimmering eyeshadow", "fresh no-makeup look"],
        "skin.txt": ["porcelain fair skin", "sun-kissed tan skin", "rich dark skin", "pale translucent skin"],
        "special_marks.txt": ["charming mole under eye", "dusting of freckles", "faded battle scar", "intricate tattoo", "distinctive beauty mark"],
        "gaze.txt": ["staring directly at viewer", "looking away distantly", "looking back over shoulder", "peacefully closed eyes"]
    },
    "hair": {
        "color.txt": ["jet black hair", "shimmering silver hair", "golden blonde hair", "pastel pink hair", "electric blue hair"],
        "length.txt": ["short cropped hair", "medium shoulder-length hair", "long flowing hair", "very long floor-length hair"],
        "style.txt": ["high ponytail", "sleek bob cut", "messy bedhead", "cute twintails", "intricate braid", "chic pixie cut", "elegant french twist", "casual messy bun", "long dreadlocks", "voluminous afro", "tight cornrows", "traditional hime cut", "edgy undercut", "punk mohawk"],
        "details.txt": ["glossy shiny hair", "decorative hair ornament", "colorful hair ribbon", "playful ahoge", "vibrant multi-colored hair", "soft gradient hair color", "magical glittering hair"]
    },
    "body": {
        "height.txt": ["tall and statuesque", "petite and cute", "average height"],
        "build.txt": ["slender model figure", "hourglass curvy figure", "toned muscular build", "soft chubby figure", "skinny frame"],
        "posture.txt": ["relaxed and casual posture", "elegant upright posture", "dynamic action pose", "slouching lazily"],
        "hands.txt": ["hands casually in pockets", "holding a smartphone", "making a V-sign", "arms crossed defensively"]
    },
    "outfit": {
        "sets": {
            "casual.txt": ["oversized hoodie", "distressed jeans", "graphic t-shirt", "denim shorts"],
            "school.txt": ["classic school uniform", "sailor uniform (seifuku)", "preppy blazer uniform", "traditional serafuku"],
            "business.txt": ["tailored business suit", "smart blazer", "tight pencil skirt", "silk tie"],
            "dress.txt": ["flowing long dress", "elegant cocktail dress", "light summer dress", "formal ball gown"],
            "sporty.txt": ["fitted sportswear", "athletic tracksuit", "gym workout clothes", "flexible yoga pants"],
            "traditional.txt": ["elaborate kimono", "flowimg hanfu", "elegant cheongsam", "summer yukata"],
            "onepiece.txt": ["floral dress", "stylish coat dress", "french maid uniform", "nurse uniform"]
        },
        "garments": {
            "top.txt": ["chiffon blouse", "cotton t-shirt", "leather jacket", "knitted sweater", "sleeveless tank top"],
            "bottom.txt": ["pleated skirt", "casual shorts", "formal pants", "mini pleated skirt", "tight leggings"],
            "shoes.txt": ["high-top sneakers", "leather boots", "high heels", "summer sandals", "classic loafers"],
            "accessories.txt": ["stylish glasses", "dangling earrings", "pearl necklace", "wide-brimmed hat", "mysterious mask"]
        },
        "attributes": {
            "color_palette.txt": ["black and white monochrome", "soft pastel colors", "bright vivid colors", "dark moody theme"],
            "material.txt": ["studded leather", "blue denim", "smooth silk", "shiny latex", "soft cotton"]
        }
    },
    "pose": {
        "base.txt": ["standing confidently", "sitting elegantly", "lying down comfortably", "kneeling gracefully", "squatting low", "floating weightlessly", "leaning against wall", "crouching in stealth", "reclining on sofa", "walking briskly", "running fast", "dancing gracefully", "fighting stance", "jumping high", "flying in sky", "swimming underwater", "reading a book intently", "eating delicious food", "drinking coffee", "aiming and shooting", "casting magic spell", "singing passionately"],
        "hand_pose.txt": ["waving hello", "peace sign", "pointing finger", "reaching out hand", "holding a weapon tightly", "hands resting on hips", "crossed arms", "military salute", "making heart shape with hands", "praying hands"],
        "dynamic.txt": ["hair flowing in wind", "dynamic motion blur", "strong wind blowing", "floating in zero gravity", "suspended in mid-air", "dramatic camera angle", "extreme perspective distortion", "dramatic foreshortening", "explosive background effect"]
    },
    "scene": {
        "location": {
            "indoor.txt": ["cozy café", "modern office", "school classroom", "messy bedroom", "ancient library", "luxury hotel suite", "cozy fireplace living room", "abandoned stone ruins", "futuristic space station interior"],
            "outdoor.txt": ["bustling city street", "peaceful park", "sunny beach", "dense forest", "futuristic cityscape", "neon-lit futuristic city", "glowing magical forest", "rainy cyberpunk street", "vast desert dunes", "snowy mountain peak", "deep underwater coral reef"]
        },
        "time.txt": ["early morning sunrise", "golden sunset", "starry night", "bright noon", "twilight dusk"],
        "weather.txt": ["bright sunny day", "heavy rainy day", "falling snow", "overcast cloudy", "thunderstorm"],
        "season.txt": ["blooming spring", "colorful autumn", "hot summer", "cold winter"],
        "background_detail.txt": ["soft bokeh background", "clean minimalist background", "colorful abstract background", "dark moody background", "bright high-key background", "intricate pattern background"],
        "props.txt": ["glowing neon signs", "bookshelves filled with books", "blooming flowers", "vintage furniture"]
    },
    "camera": {
        "shot_type.txt": ["intimate close-up", "upper body half shot", "full body shot", "classic portrait", "cowboy shot (knees up)", "extreme macro close-up", "macro detail shot", "first-person point of view", "mirror selfie"],
        "angle.txt": ["worm's eye low angle", "bird's eye high angle", "tilted dutch angle", "straight-on eye level", "top-down bird's eye view", "ground level worm's eye view", "aerial drone view", "over-the-shoulder perspective", "dynamic action angle"],
        "lens.txt": ["35mm storytelling lens", "50mm standard lens", "wide angle lens", "telephoto compression lens", "distorted fisheye lens", "gopro action view"],
        "composition.txt": ["centered composition", "rule of thirds", "symmetrical composition", "golden ratio composition"],
        "depth_of_field.txt": ["shallow depth of field (blurred background)", "creamy bokeh", "deep focus (everything sharp)", "dynamic motion blur"]
    },
    "lighting": {
        "source.txt": ["soft natural light", "dramatic rim light", "professional studio light", "bright sunlight", "divine god rays", "mystical bioluminescent glow", "harsh neon lights", "cinematic lens flare"],
        "mood.txt": ["cinematic movie lighting", "soft diffused light", "dramatic high-contrast lighting", "dark and moody atmosphere", "hazy volumetric lighting", "golden hour warm glow", "blue hour cool tones", "vibrant cyberpunk lighting", "artistic rembrandt lighting", "glamorous butterfly lighting", "chiaroscuro light and shadow", "subtle ambient occlusion"],
        "color_temp.txt": ["warm orange lighting", "cool blue lighting", "neutral white lighting"],
        "contrast.txt": ["high contrast shadows", "soft contrast", "low key darkness", "high key brightness"]
    },
    "style": {
        "medium.txt": ["photograph", "watercolor painting", "oil painting", "digital art illustration", "rough sketch", "vintage polaroid", "aged vintage photo", "grainy film photo", "black and white line art", "retro pixel art", "traditional ink wash painting", "charcoal drawing", "soft pastel art", "3d cgi render", "flat vector art", "stained glass art"],
        "genre.txt": ["futuristic cyberpunk", "high fantasy", "everyday slice of life", "sci-fi cosmos", "eldritch horror", "japanese anime style", "american comic book style", "victorian steampunk", "retro vaporwave aesthetic", "gritty noir", "dark gothic", "desolate post-apocalyptic", "vibrant 80s retro"],
        "render.txt": ["ultra detailed 8k", "high quality masterpiece", "8k resolution", "photorealistic texturing", "unreal engine 5 render", "vray raytracing", "octane render path tracing", "digital matte painting", "video game concept art"],
        "art_direction.txt": ["cinematic movie scene", "clean minimalistic", "dreamy surrealism", "abstract expressionism"],
        "quality_tags.txt": ["masterpiece artwork", "best quality illustration", "absurdres", "incredibly detailed texture"]
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
        "count.txt": ["1個女孩", "2個女孩", "單人焦點", "情侶在一起", "一群朋友"],
        "type.txt": ["人類女性", "神秘精靈", "生化仿生人", "擬人化動物", "奇幻魔物娘"],
        "role.txt": ["勤奮的學生", "忙碌的上班族", "重裝騎士", "奧術法師", "溫柔護理師"],
        "age.txt": ["充滿活力的青少年", "年輕成人", "成熟女性", "小孩", "睿智長者"],
        "ethnicity.txt": ["亞洲血統", "高加索血統", "拉丁裔血統", "非裔血統", "中東血統"],
        "vibe.txt": ["可愛萌系氛圍", "酷炫有型氛圍", "優雅精緻氛圍", "帥氣強悍氛圍", "陰鬱神秘氛圍", "開朗陽光氛圍", "神秘莫測氛圍", "憂鬱悲傷氛圍", "活力運動氛圍"],
        "clothing_style.txt": ["1920年代復古女伶風", "高科技賽博龐克機能風", "維多利亞蒸氣龐克風", "波西米亞音樂節風", "現代街頭潮流", "前衛高級時尚", "暗黑哥德蘿莉風", "舒適運動休閒風", "乾淨學院風", "90年代頹廢風", "現代極簡風"],
        "fabric.txt": ["滑順絲綢", "奢華天鵝絨", "粗曠丹寧", "光澤皮革", "緊身乳膠", "精緻蕾絲", "閃亮亮片", "粗針織毛線", "粗糙帆布", "柔滑緞面", "透氣亞麻", "半透明薄紗"]
    },
    "face": {
        "expression.txt": ["溫暖柔和的微笑", "嚴肅專注的表情", "打哈欠的睡臉", "生氣的皺眉", "害羞臉紅", "開懷大笑", "淚流滿面", "驚訝地睜大眼", "困惑地歪頭", "害怕的表情", "誘惑的眼神", "厭惡的冷笑", "無表情撲克臉", "充滿喜悅", "眼眶泛淚", "暴怒"],
        "eyes_color.txt": ["深邃棕色眼睛", "清澈藍色眼睛", "翠綠色眼睛", "寶石紅眼睛", "異色瞳(一藍一綠)"],
        "eyes_shape.txt": ["無辜大眼", "銳利細長眼", "愛睏下垂眼", "銳利吊眼", "溫柔垂眼"],
        "makeup.txt": ["自然淡妝", "哥德風濃妝", "大膽紅唇", "閃亮眼影", "清純素顏"],
        "skin.txt": ["白皙瓷肌", "古銅色肌膚", "黝黑肌膚", "蒼白肌膚"],
        "special_marks.txt": ["淚痣", "雀斑", "戰鬥舊傷疤", "精緻刺青", "美人痣"],
        "gaze.txt": ["直視觀眾", "看向遠方", "回頭看", "安詳閉眼"]
    },
    "hair": {
        "color.txt": ["烏黑秀髮", "閃耀銀髮", "金黃秀髮", "粉彩粉紅髮", "電光藍髮"],
        "length.txt": ["俐落短髮", "及肩中長髮", "飄逸長髮", "及地超長髮"],
        "style.txt": ["高馬尾", "俐落鮑伯頭", "凌亂剛睡醒髮型", "可愛雙馬尾", "精緻編髮", "俏麗精靈短髮", "優雅法式盤髮", "隨性凌亂包頭", "長髒辮", "蓬鬆爆炸頭", "緊密玉米雷鬼辮", "傳統姬髮式", "前衛削邊頭", "龐克莫霍克頭"],
        "details.txt": ["天使光環光澤髮質", "精緻髮飾", "彩色髮帶", "俏皮呆毛", "鮮豔多色挑染", "柔和漸層髮色", "魔法閃亮髮絲"]
    },
    "body": {
        "height.txt": ["如雕像般高挑", "嬌小可愛", "平均身高"],
        "build.txt": ["模特兒般纖細身材", "沙漏型曲線身材", "結實肌肉體格", "肉感身材", "骨感身材"],
        "posture.txt": ["放鬆休閒姿勢", "優雅挺立姿勢", "動態動作姿勢", "懶散駝背"],
        "hands.txt": ["雙手插口袋", "拿著智慧型手機", "比YA手勢", "雙手防衛性交叉"]
    },
    "outfit": {
        "sets": {
            "casual.txt": ["寬鬆帽T", "破損牛仔褲", "圖案T恤", "牛仔短褲"],
            "school.txt": ["經典學校制服", "水手服", "學院風西裝制服", "傳統水手服"],
            "business.txt": ["量身訂製西裝", "俐落西裝外套", "緊身鉛筆裙", "絲質領帶"],
            "dress.txt": ["飄逸長洋裝", "優雅雞尾酒禮服", "清爽夏季洋裝", "正式晚禮服"],
            "sporty.txt": ["合身運動服", "田徑服", "健身房運動服", "彈性瑜珈褲"],
            "traditional.txt": ["華麗和服", "飄逸漢服", "優雅旗袍", "夏季浴衣"],
            "onepiece.txt": ["碎花洋裝", "時尚大衣式洋裝", "法式女僕裝", "護士制服"]
        },
        "garments": {
            "top.txt": ["雪紡襯衫", "純棉T恤", "皮夾克", "針織毛衣", "無袖背心"],
            "bottom.txt": ["百褶裙", "休閒短褲", "正式長褲", "迷你百褶裙", "緊身內搭褲"],
            "shoes.txt": ["高筒運動鞋", "皮革靴子", "高跟鞋", "夏季涼鞋", "經典樂福鞋"],
            "accessories.txt": ["時尚眼鏡", "垂墜耳環", "珍珠項鍊", "寬簷帽", "神秘面具"]
        },
        "attributes": {
            "color_palette.txt": ["黑白單色系", "柔和粉色系", "鮮豔亮色系", "暗黑陰鬱色系"],
            "material.txt": ["鉚釘皮革", "藍色丹寧", "柔順絲綢", "亮面乳膠", "柔軟棉質"]
        }
    },
    "pose": {
        "base.txt": ["自信站立", "優雅坐姿", "舒適躺臥", "優雅跪姿", "低蹲", "失重漂浮", "倚靠牆壁", "隱密蹲伏", "斜躺在沙發", "輕快走路", "快速奔跑", "優雅跳舞", "戰鬥架勢", "高高跳起", "在空中飛行", "在水下游泳", "專注閱讀", "享用美食", "喝咖啡", "瞄準射擊", "施展魔法", "熱情歌唱"],
        "hand_pose.txt": ["揮手打招呼", "比YA", "手指指向前方", "伸手觸摸", "緊握武器", "雙手叉腰", "雙手交叉", "軍禮", "雙手比愛心", "雙手合十祈禱"],
        "dynamic.txt": ["頭髮隨風飄動", "強烈動態模糊", "強風吹拂", "零重力漂浮", "懸浮在半空", "戲劇性鏡頭角度", "透視極度變形", "透視縮短", "爆炸背景特效"]
    },
    "scene": {
        "location": {
            "indoor.txt": ["溫馨咖啡廳", "現代化辦公室", "學校教室", "凌亂的臥室", "古老圖書館", "豪華飯店套房", "溫馨壁爐客廳", "廢棄石造廢墟", "未來太空站內部"],
            "outdoor.txt": ["繁忙城市街道", "寧靜公園", "陽光普照海灘", "茂密森林", "未來都市景觀", "霓虹未來城市", "發光魔法森林", "雨中賽博龐克街道", "廣闊沙漠沙丘", "雪山山頂", "深海珊瑚礁"]
        },
        "time.txt": ["清晨日出", "金黃日落", "星空夜晚", "明亮正午", "暮色黃昏"],
        "weather.txt": ["晴朗豔陽天", "傾盆大雨", "飄落白雪", "陰霾多雲", "雷雨交加"],
        "season.txt": ["百花盛開春天", "多彩楓紅秋天", "炎熱夏天", "寒冷冬天"],
        "background_detail.txt": ["柔和散景背景", "乾淨極簡背景", "多彩抽象背景", "暗黑氛圍背景", "明亮高調背景", "複雜紋理背景"],
        "props.txt": ["發光霓虹燈招牌", "擺滿書的書架", "盛開花朵", "復古家具"]
    },
    "camera": {
        "shot_type.txt": ["親密特寫", "上半身鏡頭", "全身鏡頭", "經典肖像", "七分身鏡頭(膝蓋以上)", "極致微距特寫", "微距細節", "第一人稱視角(POV)", "對鏡自拍"],
        "angle.txt": ["仰視低角度", "俯視高角度", "傾斜荷蘭式鏡頭", "正面平視", "頂視鳥瞰圖", "地面仰視圖", "空拍機視角", "過肩鏡頭", "動態動作角度"],
        "lens.txt": ["35mm敘事鏡頭", "50mm標準鏡頭", "廣角鏡頭", "長焦壓縮鏡頭", "魚眼變形鏡頭", "GoPro運動視角"],
        "composition.txt": ["置中構圖", "三分法構圖", "對稱構圖", "黃金比例構圖"],
        "depth_of_field.txt": ["淺景深(背景模糊)", "柔美散景", "深焦(全景清晰)", "動態模糊"]
    },
    "lighting": {
        "source.txt": ["柔和自然光", "戲劇性輪廓光", "專業攝影棚光", "明亮陽光", "神聖耶穌光", "神秘生物發光", "刺眼霓虹燈", "電影鏡頭光暈"],
        "mood.txt": ["電影質感光線", "柔和漫射光", "戲劇性高對比光", "陰暗情緒氛圍", "朦朧體積光", "黃金時段曖曖光暈", "藍色時刻冷色調", "鮮豔賽博龐克光", "藝術倫勃朗光", "迷人蝴蝶光", "明暗對照法光影", "細微環境光遮蔽"],
        "color_temp.txt": ["溫暖橘色光", "冷冽藍色光", "中性白光"],
        "contrast.txt": ["高對比陰影", "柔和對比", "低調陰暗", "高調明亮"]
    },
    "style": {
        "medium.txt": ["攝影照片", "水彩畫", "油畫", "數位藝術插畫", "粗略素描", "復古拍立得", "老舊復古照片", "顆粒感底片照", "黑白線稿", "復古像素藝術", "傳統水墨畫", "炭筆素描", "柔和粉彩畫", "3D CGI渲染", "扁平向量圖", "彩繪玻璃藝術"],
        "genre.txt": ["未來賽博龐克", "奇幻史詩", "日常景觀", "科幻宇宙", "洛夫克拉夫特式恐怖", "日本動漫風格", "美式漫畫風格", "維多利亞蒸氣龐克", "復古蒸氣波美學", "硬派黑色電影", "暗黑哥德式", "荒涼末日後", "鮮豔80年代復古"],
        "render.txt": ["超精細8k解析度", "高品質傑作", "8k高解析度", "照片級真實紋理", "虛幻引擎5渲染", "V-Ray光線追蹤", "Octane渲染路徑追蹤", "數位繪景", "電玩概念藝術"],
        "art_direction.txt": ["電影場景感", "乾淨極簡主義", "夢幻超現實主義", "抽象表現主義"],
        "quality_tags.txt": ["大師級藝術作品", "最佳品質插畫", "超高解析度", "難以置信的細節紋理"]
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
