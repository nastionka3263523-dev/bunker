import discord
from discord.ext import commands
from discord import app_commands
import random

TOKEN = "MTQ5NzQ0NDk4OTMxMTgyNzk2OA.G0tJ86.Gl-BTnpaYZa2uuFoSpiuUlmqalxYbYvB-jSTH8"

CARDS = {
    "bagazh": {
        "count": 10,
        "name": "🎒 БАГАЖ",
        "items": ["Набір інструментів","Медична аптечка","Мішок насіння овочів","Біблія та молитовник","Рибальське спорядження","Генератор на сонячних батареях","Запас ліків на 6 місяців","Шапочка з фольги","Колекція вінілових платівок","Ноутбук з офлайн-енциклопедією"]
    },
    "biologia": {
        "count": 20,
        "name": "👤 БІОЛОГІЯ",
        "items": ["Чоловік, 22 роки, 68 кг","Жінка, 34 роки, 61 кг","Чоловік, 47 років, 91 кг","Жінка, 58 років, 74 кг","Чоловік, 19 років, 55 кг","Жінка, 26 років, 82 кг","Чоловік, 63 роки, 110 кг","Жінка, 41 рік, 57 кг","Чоловік, 35 років, 78 кг","Жінка, 17 років, 49 кг","Чоловік, 52 роки, 95 кг","Жінка, 29 років, 66 кг","Чоловік, 38 років, 83 кг","Жінка, 45 років, 71 кг","Чоловік, 71 рік, 76 кг","Жінка, 23 роки, 53 кг","Чоловік, 56 років, 102 кг","Жінка, 31 рік, 88 кг","Чоловік, 14 років, 61 кг","Жінка, 67 років, 69 кг"]
    },
    "hobbi": {
        "count": 21,
        "name": "🎯 ХОБІ",
        "items": ["Рибальство","В'язання","Полювання","Городництво та садівництво","Шахи","Народні танці","Збір грибів та ягід","Кулінарія та консервація","Радіоаматорство","Бджільництво","Різьба по дереву","Вишивка хрестиком","Стрільба з лука","Йога та медитація","Колекціонування монет","Ремонт техніки","Малювання акварелями","Фотографія природи","Гра на бандурі","Читання книг","Виготовлення свічок"]
    },
    "profesia": {
        "count": 20,
        "name": "💼 ПРОФЕСІЯ",
        "items": ["Хірург","Шахтар","Вчителька початкових класів","Програміст","Ветеринар","Кухар","Військовий сапер","Психолог","Фермер","Електрик","Акушерка","Священник","Механік","Біолог-дослідник","Пожежник","Стоматолог","Юрист","Будівельник","Медсестра","Агроном"]
    },
    "zdorovia": {
        "count": 20,
        "name": "❤️ ЗДОРОВ'Я",
        "items": ["Абсолютно здоровий","Діабет 2 типу","Астма","Відмінний імунітет","Гіпертонія","Алергія на пилок","Сколіоз","Вегетаріанець з народження","Епілепсія","Хронічний гастрит","Відсутність одного ока","Глухота на одне вухо","Безсоння хронічне","Вагітність 3 місяці","Протез лівої ноги","Алергія на антибіотики","Ожиріння 2 ступеня","Дальтонізм","Панічні атаки","Відсутність селезінки"]
    }
}

GDRIVE = "https://drive.google.com/uc?export=download&id="

FILE_IDS = {
    "bagazh": {
        1: "1KRdGtL4zO3KGvvm9eGj89U2nerVhmz8I",
        2: "1uCJiNstTtYeZaeav-_AKgBzLhFVsn7H0",
    },
    "biologia": {
        1: "16EVWQqy6Xs_MrVs7NGpyTSD3DRS7754W",
    },
    "hobbi": {
        1: "1yX8vvxE-zzloeW-lS-wgaqdS3A7_iD_R",
    },
    "profesia": {
        1: "1HFwM8kP7WzZloFGIrFYC0qGEXHFm3g6l",
    },
    "zdorovia": {
        1: "1w19woIag2j7sRCO2MUZVhvRv4QDOgcmk",
    }
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree
games = {}

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Бот {bot.user} запущено!")

@tree.command(name="бункер", description="Почати нову гру в Бункер")
async def bunker(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    games[guild_id] = {"players": {}}
    await interaction.response.send_message(
        "🏚️ **Гра в Бункер розпочата!**\nГравці — пишіть `/приєднатись`!\nВедуча пише `/старт` коли всі готові!"
    )

@tree.command(name="приєднатись", description="Приєднатись до гри")
async def join(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    user = interaction.user

    if guild_id not in games:
        await interaction.response.send_message("❌ Спочатку ведуча має написати `/бункер`!", ephemeral=True)
        return

    if user.id in games[guild_id]["players"]:
        await interaction.response.send_message("❌ Ти вже в грі!", ephemeral=True)
        return

    player_cards = {}
    for cat, data in CARDS.items():
        idx = random.randint(1, data["count"])
        player_cards[cat] = {"idx": idx, "revealed": False}

    games[guild_id]["players"][user.id] = {"name": user.display_name, "cards": player_cards}

    try:
        await user.send(
            f"🎴 **ТВОЯ КАРТКА — БУНКЕР**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"Всі категорії закриті 🔒\n"
            f"━━━━━━━━━━━━━━━\n"
            f"Щоб відкрити пиши в каналі:\n"
            f"`/відкрити багаж`\n"
            f"`/відкрити біологія`\n"
            f"`/відкрити хобі`\n"
            f"`/відкрити професія`\n"
            f"`/відкрити здоров'я`"
        )
        await interaction.response.send_message(f"✅ **{user.display_name}** приєднався! Картка надіслана 📩")
    except:
        await interaction.response.send_message("❌ Не можу надіслати повідомлення! Відкрий налаштування Discord.", ephemeral=True)

@tree.command(name="відкрити", description="Відкрити одну зі своїх карток")
@app_commands.describe(категорія="багаж / біологія / хобі / професія / здоров'я")
async def reveal(interaction: discord.Interaction, категорія: str):
    guild_id = interaction.guild_id
    user = interaction.user

    cat_map = {
        "багаж": "bagazh", "біологія": "biologia",
        "хобі": "hobbi", "професія": "profesia", "здоров'я": "zdorovia"
    }

    cat = cat_map.get(категорія.lower())
    if not cat:
        await interaction.response.send_message("❌ Невірна категорія!", ephemeral=True)
        return

    if guild_id not in games or user.id not in games[guild_id]["players"]:
        await interaction.response.send_message("❌ Ти не в грі!", ephemeral=True)
        return

    player = games[guild_id]["players"][user.id]
    card = player["cards"][cat]

    if card["revealed"]:
        await interaction.response.send_message(f"❌ Ти вже відкрив цю картку!", ephemeral=True)
        return

    card["revealed"] = True
    idx = card["idx"]
    item = CARDS[cat]["items"][idx - 1]
    name_ua = CARDS[cat]["name"]

    await interaction.response.send_message(
        f"{name_ua}\n━━━━━━━━━━━━━━━\n**{user.display_name}** відкриває:\n**{item}**"
    )

    if idx in FILE_IDS.get(cat, {}):
        file_id = FILE_IDS[cat][idx]
        url = GDRIVE + file_id
        await interaction.followup.send(url)

@tree.command(name="стоп", description="Завершити гру")
async def stop(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    if guild_id in games:
        del games[guild_id]
    await interaction.response.send_message("🏁 Гра завершена!")

bot.run(TOKEN)
