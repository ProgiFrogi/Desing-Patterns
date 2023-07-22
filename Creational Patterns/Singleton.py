# Singleton - паттер, позволяющий получать один и тот же объект за разные вызовы класса.
# Плюсы: гарантирует создание одного экземпляра класса, создает глобальную точку входа
# При многопоточности нужно синхронихировать

class DataBase:
    instance = None
    def __new__(cls, *args, **kwargs):
        if DataBase.instance is None:
            DataBase.instance = super().__new__(cls)
            DataBase._do_work(DataBase.instance)
        return DataBase.instance

    
    def _do_work(self):
        print('do some hard work')
        self.data = 110101010101