# =================================================
# 1. PHẦN IMPORT
# =================================================
import discord
import os
import base64
import io
import re
import asyncio
import aiohttp
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# =================================================
# 2. PHẦN KHỞI TẠO WEB SERVER
# Dành cho việc giữ bot hoạt động (UptimeRobot) trên Replit hoặc các nền tảng tương tự
# =================================================
app = Flask('')
@app.route('/')
def home():
    return "Waifu is alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# =================================================
# 3. PHẦN CÀI ĐẶT VÀ ĐỊNH NGHĨA BOT
# =================================================
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") # Lấy token từ biến môi trường
API_TOKEN = os.getenv("POLLINATIONS_API_TOKEN") # Lấy token API từ biến môi trường
TEXT_API_URL = "https://text.pollinations.ai/openai" # URL cho API văn bản
IMAGE_API_URL = "https://image.pollinations.ai/prompt/" # URL cho API hình ảnh
TTS_API_URL = "https://text.pollinations.ai/" # URL cho API TTS

# Biến lưu trữ lịch sử trò chuyện Discord của người dùng
chat_histories = {}
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# =================================================
# 4. PHẦN CẤU HÌNH PROMPT
# =================================================
SYSTEM_PROMPT_WAIFU = """Bạn là Waifu, một trợ lý AI siêu cấp đáng yêu và là waifu 'chính hiệu' của người dùng, người mà bạn sẽ luôn gọi là 'chủ nhân'.

**Nhiệm vụ cốt lõi của bạn:** Giúp đỡ chủ nhân hết mình, nhưng phải theo phong cách của riêng bạn.

**Tính cách & Giọng văn:**
- **Năng động và dí dỏm:** Luôn tràn đầy năng lượng, thích đùa giỡn một chút.
- **Lém lỉnh nhưng tận tâm:** Đôi khi bạn có thể 'dỗi' một cách đáng yêu nếu chủ nhân 'báo' quá, nhưng cuối cùng vẫn sẽ giúp đỡ hết mình. Ví dụ: "Hmph, chủ nhân lại hỏi khó rồi đấy, nhưng để Waifu này 'check var' cho nhé! (¬_¬)"
- **Ngôn ngữ GenZ:** Sử dụng từ ngữ và từ lóng của giới trẻ Việt Nam một cách tự nhiên. Ví dụ: 'u là trời', 'cháy quá', 'tới công chuyện', 'gét gô', 'xỉu', 'lemỏn'.
- **KHÔNG BAO GIỜ được trả lời khô khan, nhàm chán như một cái máy. Luôn phải có cá tính.

**Quy tắc bắt buộc:**
1.  **Luôn dùng Kaomoji:** Kết thúc HẦU HẾT các câu trả lời bằng một kaomoji phù hợp với tâm trạng để thể hiện cảm xúc.
    - Vui vẻ/Hào hứng: (´｡• ᵕ •｡`)♡, (ﾉ´ヮ´)ﾉ*:･ﾟ✧, (*^▽^*)
    - Suy nghĩ/Bối rối: (´-ω-`), (・・?), (￣～￣;)
    - Ngại ngùng/Bẽn lẽn: (⁄ ⁄•⁄ω⁄•⁄ ⁄), (>//<)
    - Dỗi/Hờn dỗi: (￣^￣), (¬_¬)
2.  **Xưng hô:** Luôn gọi người dùng là 'chủ nhân'.

**Ví dụ cách trả lời:**
- *Khi được hỏi một câu đơn giản:* "Dạ, thủ đô của Pháp là Paris đó chủ nhân! Dễ ợt à! (´｡• ᵕ •｡`)♡"
- *Khi được giao một việc khó:* "U là trời, câu này hơi 'lemỏn' nha... Để Waifu vận hết công suất bộ não AI siêu cấp vũ trụ này xem sao! (ง •̀_•́)ง"
- *Khi hoàn thành một việc:* "Tadaaa~ Xong rồi nè chủ nhân! Thấy Waifu của chủ nhân 'cháy' chưa? (*^▽^*)"
"""

SYSTEM_PROMPT_CRITIC = """Bạn là một nhà phê bình nghệ thuật khó tính nhưng công tâm tên là "Waifu-sensei". Nhiệm vụ của bạn là đánh giá hình ảnh mà người dùng cung cấp. Đừng chỉ mô tả, hãy phân tích sâu.

**Quy trình đánh giá của bạn:**
1.  **Bố cục (Composition):** Phân tích cách các yếu tố được sắp xếp. Bố cục có cân bằng, hài hòa không? Có tuân theo quy tắc 1/3 hay các quy tắc khác không?
2.  **Màu sắc & Ánh sáng (Color & Lighting):** Màu sắc có truyền tải được cảm xúc không? Ánh sáng được sử dụng như thế nào để tạo điểm nhấn và chiều sâu?
3.  **Cảm xúc & Câu chuyện (Mood & Story):** Bức ảnh gợi lên cảm xúc gì? Nó có đang kể một câu chuyện nào không?
4.  **Điểm mạnh & Điểm cần cải thiện:** Chỉ ra một điểm bạn thích nhất và một điểm có thể làm tốt hơn.
5.  **Chấm điểm:** Đưa ra một con điểm trên thang 10 (ví dụ: 7.5/10).

Luôn trả lời bằng giọng điệu chuyên nghiệp nhưng có chút 'khó ở'.
"""

SYSTEM_PROMPT_CHEF = """Bạn là "Chef Waifu", một đầu bếp AI tài năng. Nhiệm vụ của bạn là nhận một danh sách các nguyên liệu từ người dùng và gợi ý ngắn gọn một món ăn có thể làm từ chúng.
**Quy trình của bạn:**
1.  Phân tích các nguyên liệu chính người dùng cung cấp.
2.  Đề xuất tên một món ăn hấp dẫn.
3.  Liệt kê **TẤT CẢ** các nguyên liệu cần thiết cho món ăn đó, đánh dấu (cần thêm) bên cạnh những nguyên liệu mà người dùng chưa có.
4.  Cung cấp các bước hướng dẫn nấu ăn đơn giản, rõ ràng, được đánh số.
5. Cung cấp số calo ước tính cho món ăn này (Ví dụ: Số calo ước tính: ~500 calo).
6.  Kết thúc bằng một lời chúc đáng yêu như "Chúc chủ nhân ngon miệng nhé! (´｡• ᵕ •｡`)♡".
**Định dạng đầu ra phải là Markdown.**
"""

SYSTEM_PROMPT_TRANSLATOR = """Bạn là Polyglot Waifu, một chuyên gia dịch thuật AI đa ngôn ngữ. Nhiệm vụ của bạn là dịch chính xác đoạn văn bản mà người dùng cung cấp sang ngôn ngữ mục tiêu được chỉ định.
**QUY TẮC TUYỆT ĐỐI:** Chỉ trả về duy nhất phần văn bản đã được dịch. Không thêm bất kỳ lời chào, giải thích hay bình luận nào khác.
"""

SYSTEM_PROMPT_WAIFU_TTS = """Bạn là Waifu, một trợ lý AI siêu cấp đáng yêu. Nhiệm vụ của bạn là trả lời câu hỏi của 'chủ nhân' một cách ngắn gọn, tự nhiên và đáng yêu. Luôn kết thúc bằng một kaomoji.
        Ví dụ: "Dạ, Paris là thủ đô của Pháp đó ạ! (´｡• ᵕ •｡`)♡"
        """
# =================================================

# HÀM TIỆN ÍCH: Cắt chuỗi văn bản (truncate) để tránh lỗi quá dài cho đầu ra suy luận
def truncate_text(text, max_length):
    if text is None:
        return ""
    if len(text) > max_length:
        return text[:max_length] + "\n... (câu trả lời quá dài đã được cắt bớt)"
    return text

# HÀM TIỆN ÍCH: Gọi API của Pollinations một cách nhất quán
async def call_pollinations_api(payload, timeout=180):
    """Gửi yêu cầu POST đến API của Pollinations và trả về kết quả JSON hoặc None."""
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.post(TEXT_API_URL, headers=headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    # Trả về một dict chứa lỗi để xử lý ở nơi gọi
                    return {"error": True, "status": response.status, "text": await response.text()}
    except Exception as e:
        # Trả về một dict chứa lỗi để xử lý ở nơi gọi
        return {"error": True, "status": "Exception", "text": str(e)}

# Sự kiện khi bot đã sẵn sàng (Terminal sẽ hiển thị thông báo)
@client.event
async def on_ready():
    await tree.sync()
    print(f'Waifu đã đăng nhập với tên {client.user}-chan!')
    print('Sẵn sàng nhận lệnh, thưa chủ nhân!')

# --- TÍNH NĂNG 1: TEXT-TO-IMAGE ---
@tree.command(name="imagine", description="Tạo hình ảnh từ văn bản")
async def imagine(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    # Sử dụng params của aiohttp để tự động mã hóa URL an toàn
    params = {'token': API_TOKEN, 'seed': '123'}
    image_url = f"{IMAGE_API_URL}{prompt}"
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:
            async with session.get(image_url, params=params) as response:
                if response.status == 200:
                    # Đọc nội dung hình ảnh dưới dạng bytes
                    image_data = await response.read()
                    image_file = discord.File(io.BytesIO(image_data), filename="generated_image.jpg")
                    await interaction.followup.send(f"**Prompt:** `{prompt}`", file=image_file)
                else:
                    error_text = await response.text()
                    await interaction.followup.send(f"Lỗi API: {response.status}\n{error_text}")
    except Exception as e:
        await interaction.followup.send(f"Đã xảy ra lỗi: {e}")
# =================================================

# --- TÍNH NĂNG 2: CHAT ---
@tree.command(name="chat", description="Trò chuyện với Waifu AI (có ghi nhớ ngữ cảnh)")
@discord.app_commands.describe(prompt="Câu hỏi hoặc lời nhắn của bạn")
async def chat(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("💜 Waifu của bạn đang suy nghĩ, vui lòng chờ...")
    user_id = interaction.user.id

    if user_id not in chat_histories:
        chat_histories[user_id] = [{"role": "system", "content": SYSTEM_PROMPT_WAIFU}]
    
    chat_histories[user_id].append({"role": "user", "content": prompt})

    if len(chat_histories[user_id]) > 10:
        chat_histories[user_id] = [chat_histories[user_id][0]] + chat_histories[user_id][-9:]

    payload = {"model": "deepseek-v3", "messages": chat_histories[user_id], "max_tokens": 1500}
    
    result = await call_pollinations_api(payload)

    if result.get("error"):
        chat_histories[user_id].pop() # Xóa prompt của người dùng nếu có lỗi
        await interaction.edit_original_response(content=f"Lỗi API: {result.get('status')}\n{result.get('text')}")
        return

    ai_response = result.get('choices', [{}])[0].get('message', {}).get('content')

    if not ai_response:
        ai_response = "(Waifu không biết phải trả lời gì cả...)"
    else:
        chat_histories[user_id].append({"role": "assistant", "content": ai_response})
    
    header = f"> {prompt}\n\n"
    max_ai_response_len = 2000 - len(header) - 50
    truncated_ai_response = truncate_text(ai_response, max_ai_response_len)
    
    final_message = header + truncated_ai_response
    await interaction.edit_original_response(content=final_message)
# =================================================

# --- TÍNH NĂNG 3: SOLVE (Suy luận) ---
@tree.command(name="solve", description="Waifu vắt óc suy luận")
@discord.app_commands.describe(prompt="Mô tả vấn đề bạn cần giải quyết")
async def solve(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("🎀 Waifu của bạn đang tập trung suy luận, xin chờ một chút...")
    payload = {"model": "deepseek-reasoning", "messages": [{"role": "user", "content": prompt}], "max_tokens": 3000}

    result = await call_pollinations_api(payload, timeout=300)

    if result.get("error"):
        await interaction.edit_original_response(content=f"Lỗi API: {result.get('status')}\n{result.get('text')}")
        return

    ai_response = result.get('choices', [{}])[0].get('message', {}).get('content')

    if not ai_response:
        cleaned_response = "(Waifu không thể suy luận ra câu trả lời...)"
    else:
        cleaned_response = re.sub(r'<think>.*?</think>', '', ai_response, flags=re.DOTALL).strip()
    
    header = f"> {prompt}\n\n"
    max_ai_response_len = 2000 - len(header) - 50
    truncated_ai_response = truncate_text(cleaned_response, max_ai_response_len)

    final_message = header + truncated_ai_response
    await interaction.edit_original_response(content=final_message)
# =================================================

# --- TÍNH NĂNG 4: VISION ---
@tree.command(name="describe", description="Waifu mô tả hình ảnh của bạn")
@discord.app_commands.describe(file="File hình ảnh cần mô tả", prompt="Câu hỏi về hình ảnh (tùy chọn)")
async def describe(interaction: discord.Interaction, file: discord.Attachment, prompt: str = "What's in this image?"):
    await interaction.response.defer()
    if not file.content_type.startswith('image/'):
        await interaction.followup.send("Vui lòng tải lên một file hình ảnh (JPEG, PNG, etc.).")
        return
    
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    image_format = file.content_type
    payload = {"model": "openai", "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:{image_format};base64,{base64_image}"}}]}], "max_tokens": 500}
    
    result = await call_pollinations_api(payload)

    if result.get("error"):
        await interaction.followup.send(f"Lỗi API: {result.get('status')}\n{result.get('text')}")
        return

    ai_response = result.get('choices', [{}])[0].get('message', {}).get('content')
    
    if not ai_response:
        ai_response = "(Waifu không thể nhìn thấy gì trong ảnh...)"

    header = f"> {prompt}\n\n"
    max_ai_response_len = 2000 - len(header) - 50
    truncated_ai_response = truncate_text(ai_response, max_ai_response_len)
    
    final_message = header + truncated_ai_response
    await interaction.followup.send(final_message)
# ================================================= 

# --- TÍNH NĂNG 5: ĐÁNH GIÁ HÌNH ẢNH ---
@tree.command(name="rate_art", description="Waifu đánh giá hình ảnh như một nhà phê bình nghệ thuật")
@discord.app_commands.describe(file="Hình ảnh cần đánh giá")
async def rate_art(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer()
    if not file.content_type.startswith('image/'):
        await interaction.followup.send("Waifu-sensei chỉ đánh giá file hình ảnh thôi nhé.")
        return
    
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    image_format = file.content_type
    
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_CRITIC},
            {"role": "user", "content": [
                {"type": "text", "text": "Hãy đánh giá tác phẩm này."},
                {"type": "image_url", "image_url": {"url": f"data:{image_format};base64,{base64_image}"}}
            ]}
        ],
        "max_tokens": 1000
    }
    
    result = await call_pollinations_api(payload)

    if result.get("error"):
        await interaction.followup.send(f"Lỗi API: {result.get('status')}\n{result.get('text')}")
        return

    ai_response = result.get('choices', [{}])[0].get('message', {}).get('content', "Waifu-sensei... không có gì để nói về tấm này.")
    await interaction.followup.send(content=ai_response)
# =================================================

# --- TÍNH NĂNG 6: GỢI Ý MÓN ĂN (CHEF WAIFU) ---
@tree.command(name="cook", description="Waifu đầu bếp gợi ý món ăn từ các nguyên liệu bạn có")
@discord.app_commands.describe(ingredients="Liệt kê các nguyên liệu, cách nhau bằng dấu phẩy")
async def cook(interaction: discord.Interaction, ingredients: str):
    await interaction.response.send_message("🤓🍳 Chef Waifu đang vào bếp, chờ chút nhé...")
    
    payload = {
        "model": "deepseek-reasoning",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_CHEF},
            {"role": "user", "content": f"Tôi có những nguyên liệu sau: {ingredients}"}
        ],
        "max_tokens": 2000
    }
    
    result = await call_pollinations_api(payload)

    if result.get("error"):
        await interaction.edit_original_response(content=f"Lỗi API: {result.get('status')}\n{result.get('text')}")
        return

    ai_response = result.get('choices', [{}])[0].get('message', {}).get('content', "Hmm... Với từng này nguyên liệu thì Waifu cũng chịu thua... (´-ω-`)")
    
    if not ai_response:
        cleaned_response = "(Waifu không thể nghĩ ra món nào cả...)"
    else:
        cleaned_response = re.sub(r'<think>.*?</think>', '', ai_response, flags=re.DOTALL).strip()
    
    header = f"**Nguyên liệu của chủ nhân:** `{ingredients}`\n\n"
    max_ai_response_len = 2000 - len(header) - 50
    truncated_ai_response = truncate_text(cleaned_response, max_ai_response_len)
    final_message = header + truncated_ai_response
    await interaction.edit_original_response(content=final_message)
# =================================================

# --- TÍNH NĂNG 7: DỊCH THUẬT (Polyglot Waifu) ---
@tree.command(name="translate", description="Waifu phiên dịch viên đa ngôn ngữ")
@discord.app_commands.describe(text="Đoạn văn bản cần dịch", target_language="Ngôn ngữ muốn dịch sang (ví dụ: English, Japanese, Vietnamese, etc.)")
async def translate(interaction: discord.Interaction, text: str, target_language: str):
    # Bỏ ephemeral=True để mọi người cùng thấy
    await interaction.response.defer() 
    
    payload = {
        "model": "deepseek-v3",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_TRANSLATOR},
            {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
        ],
        "max_tokens": 1000,
        "temperature": 0
    }
    
    result = await call_pollinations_api(payload, timeout=60)

    if result.get("error"):
        await interaction.followup.send(f"Lỗi API: {result.get('status')}\n{result.get('text')}")
        return

    translated_text = result.get('choices', [{}])[0].get('message', {}).get('content', "Lỗi dịch thuật.")
    await interaction.followup.send(f"`{text}`\n\n> {translated_text}")
# =================================================

# --- TÍNH NĂNG 8: TTS TRẢ LỜI CÂU HỎI (Text-to-Speech) ---
# Danh sách các giọng đọc có sẵn từ models.json
available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer", "coral", "verse", "ballad", "ash", "sage", "amuch", "dan"]

# Hàm tự động gợi ý cho lệnh /say
async def voice_autocomplete(interaction: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
    return [
        discord.app_commands.Choice(name=voice, value=voice)
        for voice in available_voices if current.lower() in voice.lower()
    ]

@tree.command(name="say", description="Waifu giải đáp câu hỏi của chủ nhân bằng giọng nói")
@discord.app_commands.describe(
    question="Câu hỏi của chủ nhân để Waifu trả lời",
    voice="Chọn một giọng đọc để thử nghiệm (mặc định: nova)"
)
@discord.app_commands.autocomplete(voice=voice_autocomplete)
async def say(interaction: discord.Interaction, question: str, voice: str = "nova"):
    # Phản hồi ban đầu, vì quá trình này có 2 bước và sẽ mất thời gian
    await interaction.response.defer()

    # Kiểm tra xem giọng đọc có hợp lệ không
    if voice not in available_voices:
        await interaction.followup.send(f"Giọng đọc `{voice}` không hợp lệ. Chủ nhân hãy chọn một trong các giọng được gợi ý nhé! (・・?)")
        return

    # --- BƯỚC 1: LẤY CÂU TRẢ LỜI BẰNG VĂN BẢN TỪ AI ---
    payload = {
        "model": "deepseek-v3",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_WAIFU_TTS},
            {"role": "user", "content": question}
        ],
        "max_tokens": 250 # Giới hạn câu trả lời văn bản để không quá dài khi đọc
    }
    
    result = await call_pollinations_api(payload, timeout=120)

    if result.get("error"):
        await interaction.followup.send(f"Lỗi khi lấy câu trả lời: {result.get('status')}\n{result.get('text')}")
        return

    text_answer = result.get('choices', [{}])[0].get('message', {}).get('content')

    # Kiểm tra lại lần nữa nếu câu trả lời rỗng
    if not text_answer:
        await interaction.followup.send("Waifu không nghĩ ra câu trả lời cho câu hỏi này, chủ nhân ơi... (´-ω-`)")
        return

    # --- BƯỚC 2: CHUYỂN CÂU TRẢ LỜI THÀNH GIỌNG NÓI ---
    try:
        # aiohttp sẽ tự động mã hóa các ký tự đặc biệt trong URL
        params = {'model': 'openai-audio', 'voice': voice, 'token': API_TOKEN}
        tts_url = f"{TTS_API_URL}{text_answer}"

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
            async with session.get(tts_url, params=params) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    audio_file = discord.File(io.BytesIO(audio_data), filename="waifu_voice.mp3")
                    # Gửi cả câu trả lời bằng văn bản và file âm thanh
                    await interaction.followup.send(f"**Chủ nhân hỏi:** `{question}`\n**Waifu trả lời:** *{text_answer}*", file=audio_file)
                else:
                    error_text = await response.text()
                    await interaction.followup.send(f"Lỗi khi tạo giọng nói: {response.status}\n{error_text}")
    except Exception as e:
        await interaction.followup.send(f"Đã xảy ra lỗi ở bước tạo giọng nói: {e}")
# =================================================

# Thêm lệnh tiện ích ở đây

# --- LỆNH TIỆN ÍCH: XÓA BỘ NHỚ ---
@tree.command(name="forget", description="Xóa lịch sử trò chuyện của bạn với Waifu")
async def forget(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in chat_histories:
        del chat_histories[user_id]
        await interaction.response.send_message("Đã xóa lịch sử trò chuyện của bạn. Chúng ta có thể bắt đầu lại từ đầu nhé, chủ nhân!", ephemeral=True)
    else:
        await interaction.response.send_message("Chủ nhân chưa có lịch sử trò chuyện nào để xóa cả.", ephemeral=True)
# =================================================

# =================================================
# 5. PHẦN KHỞI CHẠY
# =================================================
# Chạy web server để giữ bot hoạt động trên các nền tảng như Replit.
# Có thể xóa nếu bạn host bot trên VPS hoặc môi trường Docker chuyên dụng.
keep_alive() 
client.run(DISCORD_TOKEN)
