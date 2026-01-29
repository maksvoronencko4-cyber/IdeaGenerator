import flet as ft
import urllib.request
import json
import threading
import os
from datetime import datetime


# ===== ИСТОРИЯ =====
def load_history():
    try:
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def save_history(history_list):
    try:
        if len(history_list) > 50:
            history_list = history_list[-50:]
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history_list, f, ensure_ascii=False, indent=2)
    except:
        pass

def add_to_history(idea, result):
    history_list = load_history()
    entry = {
        "id": len(history_list) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "idea": idea,
        "result": result
    }
    history_list.append(entry)
    save_history(history_list)

def delete_from_history(entry_id):
    history_list = load_history()
    history_list = [h for h in history_list if h.get("id") != entry_id]
    save_history(history_list)

def clear_all_history():
    save_history([])


# ===== ГЕНЕРАЦИЯ =====
def generate_with_ai(idea, language="ru"):
    if language == "en":
        lang_text = "Answer in English."
    else:
        lang_text = "Отвечай на русском."
    
    prompt = lang_text + "\n\nТы помощник для создателей контента. Помоги развить идею:\n\n"
    prompt += "1) РАЗВИТИЕ ИДЕИ - как сделать интереснее\n"
    prompt += "2) РЕАЛИЗАЦИЯ - программы, инструменты, план\n"
    prompt += "3) СОВЕТЫ - как снимать, эффекты\n"
    prompt += "4) ПОЧЕМУ ПОНРАВИТСЯ - аудитория\n"
    prompt += "5) 3 НАЗВАНИЯ\n\n"
    prompt += "ИДЕЯ: " + idea

    # Генерируем шаблон
    return generate_template(idea, language)


def generate_template(idea, language):
    words = idea.split()
    first_word = words[0] if words else "контент"
    
    if language == "en":
        return f"""💡 IDEA: {idea}

═══════════════════════════════════════

📌 DEVELOPMENT:
Your idea has great potential! Here's how to make it better:
• Add unique twist that nobody else does
• Include interactive elements
• Create a series for more engagement

🛠️ REALIZATION:
• Software: OBS Studio, DaVinci Resolve, CapCut
• Equipment: Good microphone, camera/screen capture
• Plan: Script → Record → Edit → Publish

🎬 TIPS:
• Start with attention-grabbing hook (first 3 seconds!)
• Keep dynamic pacing
• Add background music and effects
• Use captions for accessibility

🎯 WHY IT WILL WORK:
• Target: People interested in {first_word}
• Platform: YouTube, TikTok, Instagram
• Trend potential: High if executed well

✨ TITLE IDEAS:
1. "You Won't Believe This {first_word.capitalize()} Trick!"
2. "I Tried {first_word.capitalize()} For 24 Hours"
3. "The Ultimate {first_word.capitalize()} Guide 2024"

🚀 NEXT STEPS:
1. Create detailed script
2. Gather all resources
3. Record first version
4. Get feedback and improve"""
    else:
        return f"""💡 ИДЕЯ: {idea}

═══════════════════════════════════════

📌 РАЗВИТИЕ ИДЕИ:
Твоя идея имеет отличный потенциал! Вот как сделать её лучше:
• Добавь уникальную фишку которой нет у других
• Включи интерактивные элементы
• Сделай серию для большего вовлечения

🛠️ РЕАЛИЗАЦИЯ:
• Софт: OBS Studio, DaVinci Resolve, CapCut
• Оборудование: Хороший микрофон, камера/захват экрана
• План: Сценарий → Запись → Монтаж → Публикация

🎬 СОВЕТЫ:
• Начни с цепляющего хука (первые 3 секунды!)
• Держи динамичный темп
• Добавь фоновую музыку и эффекты
• Используй субтитры

🎯 ПОЧЕМУ ЗАЙДЁТ:
• Аудитория: Люди интересующиеся темой "{first_word}"
• Платформа: YouTube, TikTok, Instagram
• Потенциал: Высокий при хорошем исполнении

✨ ВАРИАНТЫ НАЗВАНИЙ:
1. "{first_word.capitalize()} - ты не поверишь что получилось!"
2. "Как я сделал {first_word} за 24 часа"
3. "Топ секреты {first_word} 2024"

🚀 СЛЕДУЮЩИЕ ШАГИ:
1. Напиши детальный сценарий
2. Собери все ресурсы
3. Запиши первую версию
4. Получи фидбек и улучши"""


# ===== ПРИЛОЖЕНИЕ =====
def main(page: ft.Page):
    page.title = "Генератор Идей"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#1a1a2e"
    
    card_bgcolor = "#16213e"
    primary_color = "#e94560"
    accent_color = "#0f3460"
    
    # Заголовок
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("💡 Генератор Идей", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Опиши идею — получи план реализации", size=13, color="#888888"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        ),
        padding=ft.padding.only(top=20, bottom=20)
    )
    
    # Поле ввода
    idea_field = ft.TextField(
        label="✏️ Твоя идея",
        hint_text="Например: снять ролик в майнкрафт с модами",
        width=340,
        multiline=True,
        min_lines=3,
        max_lines=5,
        bgcolor=card_bgcolor,
        filled=True
    )
    
    # Язык
    language_switch = ft.Switch(label="English", value=False)
    
    # Результат
    result_field = ft.TextField(
        multiline=True,
        min_lines=12,
        max_lines=20,
        read_only=True,
        value="👋 Привет!\n\n📝 Введи свою идею выше\n\n💡 Примеры:\n• Снять ролик в майнкрафт\n• Написать книгу\n• Сделать обзор\n• Записать музыку\n\n🚀 Нажми кнопку и получи план!",
        width=340,
        bgcolor="#0d1b2a",
        filled=True,
        text_size=13
    )
    
    # Статус
    loading = ft.ProgressRing(visible=False, width=25, height=25, color=primary_color)
    status_text = ft.Text("✅ Готов", size=13, color="#888888")
    
    # История
    history_container = ft.Column(controls=[], visible=False, spacing=8)
    history_visible = {"value": False}
    
    def toggle_history(e):
        history_visible["value"] = not history_visible["value"]
        history_container.visible = history_visible["value"]
        if history_visible["value"]:
            refresh_history()
            history_btn_text.value = "📚 Скрыть"
        else:
            history_btn_text.value = "📚 История"
        page.update()
    
    def refresh_history():
        history_container.controls.clear()
        items = load_history()
        
        if not items:
            history_container.controls.append(ft.Text("📭 Пусто", size=13, color="#888"))
        else:
            for item in reversed(items[-15:]):
                short = item.get("idea", "")[:35]
                if len(item.get("idea", "")) > 35:
                    short += "..."
                
                def make_open(i):
                    def fn(e):
                        result_field.value = i.get("result", "")
                        idea_field.value = i.get("idea", "")
                        page.update()
                    return fn
                
                def make_delete(i):
                    def fn(e):
                        delete_from_history(i.get("id"))
                        refresh_history()
                        page.update()
                    return fn
                
                row = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(short, size=12, weight=ft.FontWeight.BOLD),
                                    ft.Text(item.get("timestamp", ""), size=10, color="#666"),
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.IconButton(icon=ft.Icons.OPEN_IN_NEW, icon_size=18, on_click=make_open(item)),
                            ft.IconButton(icon=ft.Icons.DELETE, icon_size=18, icon_color="#f66", on_click=make_delete(item)),
                        ]
                    ),
                    bgcolor=accent_color,
                    border_radius=8,
                    padding=10
                )
                history_container.controls.append(row)
    
    def clear_history(e):
        clear_all_history()
        refresh_history()
        page.update()
    
    # Генерация
    def generate(e):
        idea = idea_field.value
        if not idea or not idea.strip():
            result_field.value = "⚠️ Введи идею!"
            page.update()
            return
        
        idea = idea.strip()
        loading.visible = True
        status_text.value = "⏳ Генерация..."
        result_field.value = "⏳ Создаю план..."
        page.update()
        
        def do_gen():
            try:
                lang = "en" if language_switch.value else "ru"
                result = generate_with_ai(idea, lang)
                result_field.value = result
                status_text.value = "✅ Готово!"
                add_to_history(idea, result)
            except Exception as ex:
                result_field.value = "❌ Ошибка: " + str(ex)
                status_text.value = "❌ Ошибка"
            loading.visible = False
            page.update()
        
        threading.Thread(target=do_gen, daemon=True).start()
    
    def copy_result(e):
        if result_field.value:
            page.set_clipboard(result_field.value)
            status_text.value = "📋 Скопировано!"
            page.update()
    
    def clear_all(e):
        result_field.value = ""
        idea_field.value = ""
        status_text.value = "🗑️ Очищено"
        page.update()
    
    # Кнопки
    generate_btn = ft.ElevatedButton(
        content=ft.Text("🚀 Развить идею", size=16, weight=ft.FontWeight.BOLD),
        width=340,
        height=55,
        bgcolor=primary_color,
        color="white",
        on_click=generate
    )
    
    history_btn_text = ft.Text("📚 История", size=13)
    history_btn = ft.TextButton(content=history_btn_text, on_click=toggle_history)
    clear_hist_btn = ft.TextButton(content=ft.Text("🗑️", size=13, color="#f66"), on_click=clear_history)
    
    copy_btn = ft.TextButton(content=ft.Text("📋 Копировать", size=12), on_click=copy_result)
    clear_btn = ft.TextButton(content=ft.Text("🗑️ Очистить", size=12), on_click=clear_all)
    
    # Карточки
    input_card = ft.Container(
        content=ft.Column(
            controls=[
                idea_field,
                ft.Row(controls=[language_switch], alignment=ft.MainAxisAlignment.END),
                generate_btn,
                ft.Row(controls=[loading, status_text], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        bgcolor=card_bgcolor,
        border_radius=12,
        padding=20
    )
    
    result_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("📄 Результат", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row(controls=[copy_btn, clear_btn], spacing=0)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=1, color=accent_color),
                result_field,
            ],
            spacing=10
        ),
        bgcolor=card_bgcolor,
        border_radius=12,
        padding=15,
        margin=ft.margin.only(top=15)
    )
    
    history_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=[history_btn, clear_hist_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                history_container,
            ],
            spacing=10
        ),
        bgcolor=card_bgcolor,
        border_radius=12,
        padding=15,
        margin=ft.margin.only(top=15, bottom=20)
    )
    
    page.add(
        ft.Column(
            controls=[header, input_card, result_card, history_card],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )
    )


ft.app(main)