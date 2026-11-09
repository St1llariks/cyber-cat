import flet as ft
import random
import time
import json
import os

SAVE_FILE = "cat_save.json"

# --- 15 ПАЛИТР ИЗ ТВОЕГО КОДА ---
palettes = [
    {"name": "⚡ Неоновый киберпанк", "cat": "#ff007f", "speech": "#00f0ff"},
    {"name": "🔥 Магия огня", "cat": "#ff6600", "speech": "#ffd700"},
    {"name": "🌿 Лесной дух", "cat": "#00ff33", "speech": "#79ff79"},
    {"name": "🌌 Космическая буря", "cat": "#9933ff", "speech": "#00bfff"},
    {"name": "🌅 Золотой закат", "cat": "#ffd700", "speech": "#ffb366"},
    {"name": "🩸 Кровавый киллер", "cat": "#ff0000", "speech": "#ffb6c1"},
    {"name": "🌊 Морская глубина", "cat": "#008b8b", "speech": "#add8e6"},
    {"name": "🍫 Шоколадный трюфель", "cat": "#8b4513", "speech": "#f5deb3"},
    {"name": "⚡ Электрик", "cat": "#1e90ff", "speech": "#7fff00"},
    {"name": "🌙 Сумеречный туман", "cat": "#808080", "speech": "#d8bfd8"},
    {"name": "🍬 Жвачка", "cat": "#ff1493", "speech": "#ffffe0"},
    {"name": "🍵 Матча-латте", "cat": "#556b2f", "speech": "#fdf5e6"},
    {"name": "🧊 Ледяной арктик", "cat": "#87ceeb", "speech": "#ffffff"},
    {"name": "🔮 Магический кристалл", "cat": "#4b0082", "speech": "#dda0dd"},
    {"name": "🌸 Уютный дзен", "cat": "#ffb6c1", "speech": "#faebd7"}
]

# --- 7 ФОНОВ ---
backgrounds = [
    "🏙️ Ночной кибер-город с неоновыми вывесками",
    "🏮 Уютный японский дворик под фонарями акари",
    "🌲 Таинственный хвойный лес в лучах заката",
    "🌌 Бескрайний открытый космос с кошачьими созвездиями",
    "🌊 Заброшенный пирс под шум прибоя и звезд",
    "⚡ Электрическая лаборатория безумного ученого",
    "🌸 Цветущий сад сакуры под розовой луной"
]

# --- 15 ЭМОЦИЙ ---
ARTS = {
    "normal": ("Обычная", "    /\\_/\\\n  ( o.o )\n    > ^ <"),
    "happy":  ("Обычная", "    /\\_/\\\n  ( ^.^ )\n    > ^ <"),
    "blush":  ("Обычная", "    /\\_/\\\n  ( ˘ ³˘)💖\n    > ^ <"),
    "angry":  ("Редкая", "    /\\_/\\\n  ( >.< )\n    > v <"),
    "disgust": ("Редкая", "    /\\_/\\\n  ( ¬_¬ )\n    > ^ <"),
    "sleep":  ("Редкая", "    /\\_/\\\n  ( -.- ) zZZ\n    > ^ <"),
    "shock":  ("Легендарная", "    /\\_/\\\n  ( O.O ) !\n    > o <"),
    "drunk":  ("Легендарная", "    /\\_/\\\n  ( x_x ) ~\n    > ^ <"),
    "fury":   ("Легендарная", "    /\\_/\\\n  ( #_# ) ⚡\n    > V <"),
    "ninja":  ("Легендарная", "    /\\_/\\\n  ( 👁️‿👁️)🥷\n    > ^ <"),
    "star":   ("Секретная", "   ✨/\\_/\\✨\n  ( ★.★ )\n    > 🌟 <"),
    "god":    ("Секретная", "   🌌/\\_/\\🌌\n  ( 👁️.👁️ )\n    > ⚡ <"),
    "cyber_cat": ("Секретная", "   💻/\\_/\\💻\n  ( [°_°] )\n    > 🔋 <"),
    "matrix": ("Секретная", "   🟢/\\_/\\🟢\n  ( 1.0 )\n    > 0 <"),
    "anime":  ("Секретная", "   🌸/\\_/\\🌸\n  ( ≧ᗜ≦)\n    > 🍡 <")
}

def main(page: ft.Page):
    page.title = "Cyberpunk Cat 🐾 (Save System)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 460
    page.window_height = 860
    page.bgcolor = "#0f0f13"

    # Проверяем, есть ли готовое сохранение
    saved_data = None
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
        except:
            pass

    # --- ЭКРАН НАСТРОЙКИ (ИЛИ КНОПКА ЗАГРУЗКИ) ---
    setup_card = ft.Container(padding=20, border_radius=20, bgcolor="#1a1a24", width=420)
    
    name_input = ft.TextField(label="Как назовем котика?", value="DifikulGamer", text_size=13)
    palette_dropdown = ft.Dropdown(
        label="🎨 Выбери цветовую палитру",
        options=[ft.dropdown.Option(str(i), p["name"]) for i, p in enumerate(palettes)],
        value="0", text_size=12
    )
    bg_dropdown = ft.Dropdown(
        label="🏞️ Выбери виртуальный фон",
        options=[ft.dropdown.Option(str(i), bg) for i, bg in enumerate(backgrounds)],
        value="0", text_size=12
    )

    setup_content = ft.Column([
        ft.Text("⚡ НАСТРОЙКА КИБЕР-ПИТОМЦА ⚡", color="#ff007f", weight=ft.FontWeight.BOLD, size=15),
        ft.Divider(color="#33334d"),
        name_input,
        palette_dropdown,
        bg_dropdown,
    ], spacing=15)

    def start_game(e, loaded_state=None):
        if loaded_state:
            cat_name = loaded_state["name"]
            pal = loaded_state["palette"]
            bg_name = loaded_state["bg"]
            build_game_ui(cat_name, pal, bg_name, loaded_state)
        else:
            cat_name = name_input.value.strip() or "DifikulGamer"
            if cat_name.lower() in ["difikulgamer", "дификул", "difikul"]:
                cat_name = "👑 DifikulGamer (Легендарный Создатель)"
            elif cat_name.lower() in ["admin", "root", "god"]:
                cat_name = "⚡ GodMode Cat"

            pal = palettes[int(palette_dropdown.value)]
            bg_name = backgrounds[int(bg_dropdown.value)]
            build_game_ui(cat_name, pal, bg_name, None)

    start_btn = ft.Button(content=ft.Text("Запустить новый мир 🚀"), on_click=lambda e: start_game(e, None), bgcolor="#00f0ff")
    setup_content.controls.append(start_btn)

    # Если есть сейв, добавляем кнопку загрузки
    if saved_data:
        load_btn = ft.Button(
            content=ft.Text(f"📂 Загрузить игру ({saved_data['name']})", color="#000000"), 
            bgcolor="#00ff66",
            on_click=lambda e: start_game(e, saved_data)
        )
        setup_content.controls.insert(2, load_btn)

    setup_card.content = setup_content
    page.add(setup_card)

    # --- ИГРОВОЙ ЭКРАН ---
    def build_game_ui(cat_name, pal, bg_name, loaded_state):
        page.clean()

        theme_state = {"dark": True}
        themes = {
            "dark": {"page_bg": "#0f0f13", "card_bg": "#1a1a24", "divider": "#33334d"},
            "light": {"page_bg": "#f0f0f5", "card_bg": "#ffffff", "divider": "#cccccc"}
        }

        if loaded_state:
            cat = loaded_state["cat"]
            action_uses = loaded_state["action_uses"]
        else:
            cat = {
                "name": cat_name,
                "energy": 7, "max_energy": 7,
                "mood": 100, "love": 0, "uses_left": 7,
                "is_sleeping": False, "fed_steak": False,
                "sleep_start_time": None, "toilet_counter": 0,
                "belly_rubs_count": 0
            }
            questions_dict = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": "", "11": "", "0": ""}
            angry_dict = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": ""}
            action_uses = {f"1_{k}": 0 for k in questions_dict.keys()}
            action_uses.update({f"2_{k}": 0 for k in angry_dict.keys()})

        art_text = ft.Text(ARTS["normal"][1], font_family="Consolas", size=20, color=pal["cat"])
        bg_text = ft.Text(f"🏞️ ФОН: {bg_name}", size=11, color="#8888aa", italic=True)
        rarity_badge = ft.Text("💫 [ОБЫЧНАЯ ЭМОЦИЯ: NORMAL]", color="#00f0ff", size=11, weight=ft.FontWeight.BOLD)
        speech_text = ft.Text(f"🐾 {cat['name']}: С возвращением в систему!", color=pal["speech"], size=14, italic=True, text_align=ft.TextAlign.CENTER)
        status_text = ft.Text(f"🔋 Энергия: {cat['uses_left']}/{cat['max_energy']} | ✨ Настроение: {cat['mood']}% | ❤️ Дружба: {cat['love']}", color="#00f0ff", size=12)

        main_card = ft.Container(padding=15, border_radius=20, bgcolor="#1a1a24", width=430)
        divider1 = ft.Divider(color="#33334d")
        divider2 = ft.Divider(color="#33334d")
        action_label = ft.Text("Выберите действие:", size=12, color="#00f0ff")
        grid_container = ft.Column(scroll=ft.ScrollMode.AUTO, height=230, spacing=6)

        questions_dict = {
            "1": "Спросить, как прошел день (вайбчек)",
            "2": "Предложить погладить за ушком",
            "3": "Поиграть в догонялки с клубочком",
            "4": "Почесать котячье пузико (Осторожно: ловушка!)",
            "5": "Накормить премиум-суши с лососем",
            "6": "Мини-игра: Угадай число (1-3)",
            "7": "Мини-игра: Камень, ножницы, лапа ✂️",
            "8": "Мини-игра: Поймай кибер-муху 🪰",
            "9": "Запустить квантовый калькулятор цундэре 🧮",
            "10": "Посветить лазерной указкой в стену 🔴",
            "11": "Отправить котика в экзистенциальный лоток 🧻",
            "0": "[СЕКРЕТНО] Взломать систему лапкой 💻"
        }

        angry_dict = {
            "1": "Спросить, почему он такой токсичный дед",
            "2": "Рискнуть пальцами и дернуть за хвост",
            "3": "Заставить его отрабатывать ипотеку за вискас",
            "4": "Напомнить, кто в этом доме открывает консервы",
            "5": "Врубить громкую музыку, чтобы позлить кота",
            "6": "Предложить ему пройти сеанс кошачьего психолога",
            "7": "Погрозить пальцем и прочитать лекцию о дисциплине",
            "8": "Экстренно отправить в лоток за отвратительное поведение"
        }

        def save_game():
            data = {
                "name": cat_name,
                "palette": pal,
                "bg": bg_name,
                "cat": cat,
                "action_uses": action_uses
            }
            try:
                with open(SAVE_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print("Ошибка сохранения:", e)

        def apply_theme():
            t = themes["dark"] if theme_state["dark"] else themes["light"]
            page.bgcolor = t["page_bg"]
            main_card.bgcolor = t["card_bg"]
            divider1.color = t["divider"]
            divider2.color = t["divider"]
            page.update()

        def toggle_theme(e):
            theme_state["dark"] = not theme_state["dark"]
            apply_theme()

        def update_view(emo, message):
            rarity_type, art_str = ARTS.get(emo, ARTS["normal"])
            art_text.value = art_str
            rarity_badge.value = f"💫 [{rarity_type.upper()} ЭМОЦИЯ: {emo.upper()}]"
            speech_text.value = f"🐾 {cat['name']}: {message}"
            status_text.value = f"🔋 Энергия: {cat['uses_left']}/{cat['max_energy']} | ✨ Настроение: {cat['mood']}% | ❤️ Дружба: {cat['love']}"
            rebuild_buttons()
            save_game()  # Автосохранение при каждом обновлении
            page.update()

        def get_random_emotion():
            roll = random.random() * 100
            if roll < 20: return "normal"
            elif roll < 40: return "happy"
            elif roll < 50: return "blush"
            elif roll < 60: return "angry"
            elif roll < 70: return "disgust"
            elif roll < 80: return "sleep"
            elif roll < 86: return "shock"
            elif roll < 92: return "drunk"
            elif roll < 96: return "fury"
            elif roll < 99: return "ninja"
            else: return "star"

        def handle_action(aid):
            if cat["uses_left"] <= 0:
                cat["is_sleeping"] = True
                show_sleep_screen()
                return

            table_num = "2" if cat["fed_steak"] else "1"
            key_id = f"{table_num}_{aid}"
            
            if action_uses[key_id] >= 2:
                update_view("angry", "❌ Этот вариант уже использован 2 раза!")
                return

            action_uses[key_id] += 1
            cat["uses_left"] -= 1
            emo = get_random_emotion()

            if not cat["fed_steak"]:
                if aid == "1":
                    cat["mood"] += 5
                    update_view(emo, random.choice(["День прошел имбово! Чилил и осуждал голубей.", "Спал 18 часов, потом смотрел в стену с ужасом."]))
                elif aid == "2":
                    cat["mood"] += 10; cat["love"] += 5
                    update_view("blush", "Мурчит как турбодизель! Твои пальцы одобрены котом. ❤️")
                elif aid == "3":
                    cat["mood"] += 8
                    update_view(emo, "Носится за клубочком быстрее пингвина от тюленя! 🧶💨")
                elif aid == "4":
                    cat["belly_rubs_count"] += 1
                    if cat["belly_rubs_count"] >= 2:
                        cat["mood"] += 50; cat["belly_rubs_count"] = 0
                        update_view("star", "ПАСХАЛКА: Чит-код на обнимашки разблокирован! 🌟🎉")
                    else:
                        if random.choice([True, False]):
                            cat["mood"] -= 15
                            update_view("fury", "КУСЬ! Это была ловушка для слабаков! Получай урон в ладонь! 😾")
                        else:
                            cat["mood"] += 25; cat["love"] += 10
                            update_view("anime", "Невероятно... Пузико открыто без кровопролития. Ты бог дипломатии! 🌸")
                elif aid == "5":
                    cat["mood"] += 20
                    update_view("happy", "Уплетает премиум-суши с лососем! «Это шедевр!» 🍣🔥")
                elif aid == "6":
                    update_view(emo, f"Загадал число от 1 до 3. Пусть будет {random.randint(1, 3)}! Угадал? 😎")
                elif aid == "7":
                    update_view("ninja", f"Дуэль КНЛ! Я выбросил {random.choice(['камень', 'ножницы', 'бумага'])}!")
                elif aid == "8":
                    if random.random() < 0.7:
                        cat["mood"] += 15
                        update_view("happy", "ХЛОП! Кибер-муха повержена лапой! 🪰🔥")
                    else:
                        update_view("drunk", "Промах... Муха затроллила нас и улетела.")
                elif aid == "9":
                    update_view("normal", "Квантовый калькулятор насчитал коэффициент крутости: 99%. База!")
                elif aid == "10":
                    cat["mood"] += 15
                    update_view("cyber_cat", "КРАСНАЯ ТОЧКА! АКТИВАЦИЯ ПРОТОКОЛА БЕЗУМИЯ НА ШТОРУ! 🔴")
                elif aid == "11":
                    cat["toilet_counter"] += 1; cat["mood"] -= 10
                    if cat["toilet_counter"] == 3:
                        update_view("matrix", "⚡ ПАСХАЛКА: Гоняешь кота в лоток 3-й раз! Открылся астральный портал!")
                    else:
                        update_view("disgust", f"Сделал токсичное лицо и пошел в лоток (Траектория №{cat['toilet_counter']}).")
                elif aid == "0":
                    cat["mood"] = 100; cat["uses_left"] += 2
                    update_view("matrix", "🕶️ [СЕКРЕТНЫЙ ПРОТОКОЛ]: Кот за 2 сек взломал Пентагон! +100 уважения.")
            else:
                if aid == "1": update_view(emo, "Потому что вокруг одни зумеры и никто не откроет влажный корм!")
                elif aid == "2": update_view("fury", "РУКИ ПРОЧЬ ОТ МОЕГО СВЯЩЕННОГО ХВОСТА! 😾⚡")
                elif aid == "3": update_view("disgust", "Работать? Моя работа — лежать и выглядеть угрожающе.")
                elif aid == "4": update_view("normal", "Ладно, признаю, консервы ты открывать умеешь сносно.")
                elif aid == "5": update_view("fury", "Выключи эту какофонию, пока я не перегрыз провода! 🎸")
                elif aid == "6": update_view("shock", "Психолог?! Да мне самому выписывать рецепты этому миру! 🛋️")
                elif aid == "7": update_view("disgust", "Лекции мне читать вздумал? Сними тапки, смертный! 📜")
                elif aid == "8": update_view("fury", "ДА ТЫ ИЗДЕВАЕШЬСЯ?! Ночью жди мести в тапки! 😾💢")

            if cat["uses_left"] <= 0:
                cat["is_sleeping"] = True
                show_sleep_screen()

        def show_sleep_screen():
            grid_container.controls.clear()
            art_text.value = ARTS["sleep"][1]
            rarity_badge.value = "💫 [РЕДКИЙ СОН: SLEEP]"
            speech_text.value = f"🐾 {cat['name']} сладко посапывает... 💤"
            
            wake_label = ft.Text("Разбудить досрочно:", color="#00f0ff", size=13)
            b1 = ft.Button(content=ft.Text("🥩 Стейк (3 энергии)"), on_click=lambda e: wake_up(1))
            b2 = ft.Button(content=ft.Text("🌿 Кошачья мята (3 энергии)"), on_click=lambda e: wake_up(2))
            b3 = ft.Button(content=ft.Text("🔋 Энергетик (+20стр)"), on_click=lambda e: wake_up(3))
            
            grid_container.controls = [wake_label, b1, b2, b3]
            page.update()

        def wake_up(method):
            cat["is_sleeping"] = False
            cat["fed_steak"] = True
            cat["max_energy"] = 3
            cat["uses_left"] = 3
            for k in angry_dict.keys(): action_uses[f"2_{k}"] = 0
            
            if method == 1: update_view("happy", "Ну ладно, стейк принят. Режим вредины! 🥩")
            elif method == 2: update_view("fury", "Р-Р-Р! МЯТА! СЛЫШУ ДВИЖЕНИЕ АТОМОВ! ⚡")
            elif method == 3:
                cat["mood"] += 20
                update_view("cyber_cat", "ЭНЕРГЕТИК УСВОЕН. БАЛАНС НАРУШЕН. 🔋")

        def rebuild_buttons():
            if cat["is_sleeping"]: return
            grid_container.controls.clear()
            table_num = "2" if cat["fed_steak"] else "1"
            current_dict = angry_dict if cat["fed_steak"] else questions_dict
            
            for k, text in current_dict.items():
                uses = action_uses[f"{table_num}_{k}"]
                btn = ft.Button(
                    content=ft.Text(f"[{k}] {text} ({uses}/2)", size=11, color="#ffffff"),
                    bgcolor="#2a2a3d" if uses < 2 else "#4a1a1a",
                    on_click=lambda e, aid=k: handle_action(aid)
                )
                grid_container.controls.append(btn)

        theme_btn = ft.Button(content=ft.Text("☀️ / 🌙 Тема", size=11), on_click=toggle_theme)
        rebuild_buttons()

        main_card.content = ft.Column([
            ft.Row([ft.Text(f"⚡ {cat['name']} ⚡", color=pal["cat"], weight=ft.FontWeight.BOLD, size=15), theme_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bg_text,
            divider1,
            art_text,
            rarity_badge,
            ft.Container(height=4),
            speech_text,
            ft.Container(height=4),
            status_text,
            divider2,
            action_label,
            grid_container
        ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        page.add(main_card)
        apply_theme()

ft.run(main)