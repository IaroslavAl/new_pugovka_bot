class Localization:
    # --- main_menu ---
    main_menu_intro = (
        "👋 <b>Добро пожаловать в наш Telegram-бот!</b>\n\n"
        "Здесь вы найдете мастер-классы, видео-курсы, выкройки и ответы на частые вопросы.\n"
        "Выберите раздел из меню ниже 👇"
    )

    # --- main_menu buttons ---
    section_personal_button = "👤 Личный кабинет"
    section_masterclasses_button = "🧵 Мастер-классы"
    section_videocourses_button = "🎥 Видео-курсы"
    section_patterns_button = "📐 Выкройки"
    section_support_button = "❓ Помощь"

    # --- prompts ---
    prompt_choose_category = "Выберите категорию:"
    prompt_category_materials = "Материалы категории: {category_name}"

    # --- personal cabinet ---
    personal_cabinet_intro = (
        "👤 <b>Личный кабинет</b>\n\n"
        "Здесь вы можете просмотреть все ваши приобретенные материалы:\n"
        "• Мастер-классы\n"
        "• Видео-курсы\n"
        "• Выкройки\n\n"
        "Выберите раздел для просмотра:"
    )

    personal_no_masterclasses = (
        "📚 <b>Мои мастер-классы</b>\n\n"
        "У вас пока нет приобретенных мастер-классов.\n"
        "Перейдите в главное меню, чтобы выбрать и приобрести интересующие вас материалы."
    )

    personal_no_videocourses = (
        "🎥 <b>Мои видео-курсы</b>\n\n"
        "У вас пока нет приобретенных видео-курсов.\n"
        "Перейдите в главное меню, чтобы выбрать и приобрести интересующие вас материалы."
    )

    personal_no_patterns = (
        "📐 <b>Мои выкройки</b>\n\n"
        "У вас пока нет приобретенных выкроек.\n"
        "Перейдите в главное меню, чтобы выбрать и приобрести интересующие вас материалы."
    )

    personal_masterclasses_title = "🧵 <b>Мои мастер-классы</b>\n\nВыберите категорию:"
    personal_videocourses_title = "🎥 <b>Мои видео-курсы</b>\n\nВыберите категорию:"
    personal_patterns_title = "📐 <b>Мои выкройки</b>\n\nВыберите категорию:"

    personal_category_materials = (
        "📂 <b>{category_name}</b>\n\nВаши материалы в этой категории:"
    )

    personal_statistics = (
        "📊 <b>Статистика покупок</b>\n\n"
        "🧵 Мастер-классы: {masterclasses_count}\n"
        "🎥 Видео-курсы: {videocourses_count}\n"
        "📐 Выкройки: {patterns_count}\n\n"
        "💰 Всего приобретено: {total_count} материалов"
    )

    # --- purchase ---
    purchase_success = "✅ <b>Покупка успешно совершена!</b>\n\nТовар <b>{item_title}</b> добавлен в ваш личный кабинет."
    purchase_already_owned = (
        "ℹ️ <b>Товар уже куплен</b>\n\nЭтот материал уже есть в вашем личном кабинете."
    )
    purchase_error = (
        "❌ <b>Ошибка покупки</b>\n\nНе удалось совершить покупку. Попробуйте еще раз."
    )

    # --- buttons ---
    buy_button = "🛒 Купить"
    open_button = "📖 Открыть"
    purchased_label = "✅ Куплено"

    # --- navigation ---
    back_button = "🔙 Назад"
    back_to_list_button = "🔙 К списку"
    back_to_main_menu_button = "🔙 Главное меню"
    go_to_purchases_button = "🛒 Перейти к покупкам"

    # --- item details ---
    item_type_masterclass = "мастер-класс"
    item_type_videocourse = "видео-курс"
    item_type_pattern = "выкройку"

    item_status_purchased = "✅ Куплено"
    item_status_available = "🛒 Доступно для покупки"

    item_description_label = "📝 <b>Описание:</b>"
    item_category_label = "📂 <b>Категория:</b>"
    item_status_label = "📊 <b>Статус:</b>"
    item_purchase_date_label = "📅 <b>Дата покупки:</b>"

    item_help_text = "Это {item_type} поможет вам освоить новые навыки шитья!"

    # --- personal cabinet buttons ---
    personal_my_masterclasses_button = "🧵 Мои мастер-классы"
    personal_my_videocourses_button = "🎥 Мои видео-курсы"
    personal_my_patterns_button = "📐 Мои выкройки"
    personal_statistics_button = "📊 Статистика покупок"

    # --- personal cabinet actions ---
    open_material_button = "🔗 Открыть материал"

    # --- errors ---
    bot_not_initialized_error = "Bot не инициализирован"
