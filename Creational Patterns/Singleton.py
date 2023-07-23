# Singleton - паттер, позволяющий получать один и тот же объект за разные вызовы класса.
# Плюсы: гарантирует создание одного экземпляра класса, создает глобальную точку входа
# При многопоточности нужно синхронихировать
#1й - из ютуба
class DataBase1:
    instance = None
    def __new__(cls, *args, **kwargs):
        if DataBase1.instance is None:
            DataBase1.instance = super().__new__(cls)
            DataBase1._do_work(DataBase1.instance)
        return DataBase1.instance

    
    def _do_work(self):
        print('do some hard work')
        self.data = 110101010101

class DataBase2:
    """
    При желании можно сделать метаклассом и наследоваться
    от него
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное
        изменение передаваемых аргументов в '__init__'
        """

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

#Многопоточный паттерн + метакласс

from threading import  Lock, Thread

class SingletonMeta(type):

    _instances = {}

    _lock: Lock = Lock()
    """
     У нас теперь есть объект-блокировка для синхронизации потоков во время
    первого доступа к Singleton
    """

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        # Теперь представьте, что программа была только-только запущена.
        # Объекта-одиночки ещё никто не создавал, поэтому несколько потоков
        # вполне могли одновременно пройти через предыдущее условие и достигнуть
        # блокировки. Самый быстрый поток поставит блокировку и двинется внутрь
        # секции, пока другие будут здесь его ожидать.
        with cls._lock:
            # Первый поток достигает этого условия и проходит внутрь, создавая
            # объект-одиночку. Как только этот поток покинет секцию и освободит
            # блокировку, следующий поток может снова установить блокировку и
            # зайти внутрь. Однако теперь экземпляр одиночки уже будет создан и
            # поток не сможет пройти через это условие, а значит новый объект не
            # будет создан.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    value: str = None
    """
    Мы используем это поле, чтобы доказать, что наш Одиночка действительно
    работает.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        """
        Наконец, любой одиночка должен содержать некоторую бизнес-логику,
        которая может быть выполнена на его экземпляре.
        """

db1 = DataBase1
db1.data = 15
db2 = DataBase1
db2.data = 40
print(db1.data)