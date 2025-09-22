from typing import Dict, List
from personal_cabinet.models import UserProfile, Purchase, PurchaseType
from content_section.data import masterclasses, videocourses, patterns


class UserService:
    def __init__(self):
        # Имитация базы данных пользователей
        self.users: Dict[int, UserProfile] = {}
        # Добавляем тестовые данные для демонстрации
        self._init_test_data()

    def _init_test_data(self):
        """Инициализация тестовых данных для демонстрации"""
        # Примерные покупки для тестирования
        test_purchases = [
            Purchase(
                id="masterclass_1",
                purchase_type=PurchaseType.masterclass,
                title="Футболка с нуля",
                description="Учимся шить базовую футболку с нуля, выбираем ткань и фурнитуру.",
                link="https://example.com/masterclass1",
                category="Рубашки и футболки",
                purchase_date="2024-01-15",
                photo_url="https://picsum.photos/200/300?random=1",
            ),
            Purchase(
                id="videocourse_5",
                purchase_type=PurchaseType.videocourse,
                title="Летнее платье с воланами",
                description="Создаем легкое платье с красивыми воланами на рукавах.",
                link="https://example.com/videocourse5",
                category="Платья",
                purchase_date="2024-02-10",
                photo_url="https://picsum.photos/200/300?random=5",
            ),
            Purchase(
                id="pattern_16",
                purchase_type=PurchaseType.pattern,
                title="Юбка-карандаш 🔥",
                description="Классическая выкройка юбки, подходящая для офиса и вечерних выходов.",
                link="https://example.com/pattern16",
                category="Юбки",
                purchase_date="2024-03-05",
                photo_url="https://picsum.photos/200/300?random=16",
            ),
        ]

        # Создаем тестового пользователя (можно использовать любой user_id для тестирования)
        test_user = UserProfile(
            user_id=12345,
            username="test_user",
            first_name="Тест",
            last_name="Пользователь",
            purchases=test_purchases,
        )
        self.users[12345] = test_user

    def get_or_create_user(
        self,
        user_id: int,
        username: str = "",
        first_name: str = "",
        last_name: str = "",
    ) -> UserProfile:
        """Получить или создать профиль пользователя"""
        if user_id not in self.users:
            # Создаем тестовые покупки для любого нового пользователя (для демонстрации)
            test_purchases = [
                Purchase(
                    id="masterclass_1",
                    purchase_type=PurchaseType.masterclass,
                    title="Футболка с нуля",
                    description="Учимся шить базовую футболку с нуля, выбираем ткань и фурнитуру.",
                    link="https://example.com/masterclass1",
                    category="Рубашки и футболки",
                    purchase_date="2024-01-15",
                    photo_url="https://picsum.photos/200/300?random=1",
                ),
                Purchase(
                    id="videocourse_5",
                    purchase_type=PurchaseType.videocourse,
                    title="Летнее платье с воланами",
                    description="Создаем легкое платье с красивыми воланами на рукавах.",
                    link="https://example.com/videocourse5",
                    category="Платья",
                    purchase_date="2024-02-10",
                    photo_url="https://picsum.photos/200/300?random=5",
                ),
                Purchase(
                    id="pattern_16",
                    purchase_type=PurchaseType.pattern,
                    title="Юбка-карандаш 🔥",
                    description="Классическая выкройка юбки, подходящая для офиса и вечерних выходов.",
                    link="https://example.com/pattern16",
                    category="Юбки",
                    purchase_date="2024-03-05",
                    photo_url="https://picsum.photos/200/300?random=16",
                ),
            ]

            self.users[user_id] = UserProfile(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                purchases=test_purchases,
            )
        return self.users[user_id]

    def add_purchase(
        self, user_id: int, item_id: str, purchase_type: PurchaseType
    ) -> bool:
        """Добавить покупку пользователю"""
        user = self.get_or_create_user(user_id)

        # Проверяем, не куплен ли уже этот товар
        if user.has_purchase(item_id):
            return False

        # Получаем данные товара из соответствующего источника
        item_data = None
        if purchase_type == PurchaseType.masterclass:
            item_data = masterclasses.get(item_id)
        elif purchase_type == PurchaseType.videocourse:
            item_data = videocourses.get(item_id)
        elif purchase_type == PurchaseType.pattern:
            item_data = patterns.get(item_id)

        if not item_data:
            return False

        # Создаем объект покупки
        purchase = Purchase(
            id=item_id,
            purchase_type=purchase_type,
            title=item_data["title"],
            description=item_data["description"],
            link=item_data["link"],
            category=item_data["category"],
            purchase_date="2024-09-22",  # В реальном приложении - текущая дата
            photo_url=item_data.get("photo_url", ""),
        )

        user.purchases.append(purchase)
        return True

    def get_user_purchases(self, user_id: int) -> List[Purchase]:
        """Получить все покупки пользователя"""
        user = self.get_or_create_user(user_id)
        return user.purchases

    def get_user_purchases_by_type(
        self, user_id: int, purchase_type: PurchaseType
    ) -> List[Purchase]:
        """Получить покупки пользователя по типу"""
        user = self.get_or_create_user(user_id)
        return user.get_purchases_by_type(purchase_type)

    def get_purchase_categories(
        self, user_id: int, purchase_type: PurchaseType
    ) -> List[str]:
        """Получить категории покупок пользователя по типу"""
        purchases = self.get_user_purchases_by_type(user_id, purchase_type)
        return list(set(p.category for p in purchases))

    def get_category_by_index(
        self, user_id: int, purchase_type: PurchaseType, category_index: int
    ) -> str:
        """Получить название категории по индексу"""
        categories = self.get_purchase_categories(user_id, purchase_type)
        if 0 <= category_index < len(categories):
            return categories[category_index]
        return ""

    def get_purchase_by_index_in_category(
        self, user_id: int, purchase_type: PurchaseType, category: str, item_index: int
    ) -> Purchase:
        """Получить покупку по индексу в рамках категории"""
        purchases = self.get_purchases_by_category(user_id, purchase_type, category)
        if 0 <= item_index < len(purchases):
            return purchases[item_index]
        return None

    def get_category_index_by_name(
        self, user_id: int, purchase_type: PurchaseType, category_name: str
    ) -> int:
        """Получить индекс категории по её названию"""
        categories = self.get_purchase_categories(user_id, purchase_type)
        try:
            return categories.index(category_name)
        except ValueError:
            return -1

    def get_purchases_by_category(
        self, user_id: int, purchase_type: PurchaseType, category: str
    ) -> List[Purchase]:
        """Получить покупки пользователя по типу и категории"""
        purchases = self.get_user_purchases_by_type(user_id, purchase_type)
        return [p for p in purchases if p.category == category]


# Глобальный экземпляр сервиса
user_service = UserService()
