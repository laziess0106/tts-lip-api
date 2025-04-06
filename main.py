from fastapi import FastAPI, Query
from fastapi.responses import Response
from g2pk import G2p
from hangul_utils import split_syllables

app = FastAPI()
g2p = G2p()

# viseme ID에 따른 SVG 예시
viseme_svgs = {
    0: "<svg width='100' height='100'><circle cx='50' cy='50' r='40' fill='red'/></svg>",
    1: "<svg width='100' height='100'><rect x='20' y='40' width='60' height='20' fill='blue'/></svg>",
    2: "<svg width='100' height='100'><ellipse cx='50' cy='50' rx='30' ry='15' fill='green'/></svg>",
    3: "<svg width='100' height='100'><polygon points='30,20 70,20 50,80' fill='purple'/></svg>",
    4: "<svg width='100' height='100'><line x1='20' y1='50' x2='80' y2='50' stroke='orange' stroke-width='5'/></svg>",
    5: "<svg width='100' height='100'><text x='10' y='50' font-size='14'>Unknown</text></svg>"
}

# 자모 → 입모양 ID 매핑
viseme_map = {
    "ㅂ": 0, "ㅁ": 0, "ㅍ": 0,
    "ㅏ": 1, "ㅑ": 1,
    "ㅓ": 2, "ㅕ": 2,
    "ㅗ": 3, "ㅛ": 3, "ㅜ": 3, "ㅠ": 3,
    "ㅅ": 4, "ㅈ": 4, "ㅊ": 4,
    "default": 5
}

@app.get("/lipshape")
def get_lip_svg(text: str = Query(...)):
    pronounced = g2p(text)        # 예: "토스트" → "토스트"
    decomposed = split_syllables(pronounced)  # "토" → "ㅌㅗ"

    first_mo = ""  # 첫 모음만 추출
    for ch in decomposed:
        if ch in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ":
            first_mo = ch
            break

    viseme_id = viseme_map.get(first_mo, viseme_map["default"])
    svg = viseme_svgs.get(viseme_id, viseme_svgs[5])
    return Response(content=svg, media_type="image/svg+xml")
