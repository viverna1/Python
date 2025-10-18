import math
import time


class Hive:
    def __init__(self, name='Улей', level=1):
        self.name = name
        self.level = level

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f'Объект класса Hive: (название: {self.name}, уровень: {self.level})'


class HoneyBeehive(Hive):
    def __init__(self, bee_count=0, name='Медовый улей', level=1, collected_honey=0, last_update_time=time.time()):
        super().__init__(name, level)
        self.bee_count = bee_count
        self.collected_honey = collected_honey
        self.last_update_time = last_update_time
        self.production_speed = self.bee_count * 0.2  # скорость производства мёда

    def __str__(self):
        self.update()  # обновляем количество собранного мёда

        attributes = [self.name + ':',  # название улья
                      'уровень: ' + str(self.level),  # уровень улья
                      'скорость производства: ' + str(math.floor(self.production_speed**0.9)),
                      'собрано меда: ' + str(math.floor(self.collected_honey)),  # количество собранного мёда
                      ]

        return '\n    '.join(attributes)

    def update(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time

        # Логистическая функция для расчета прироста меда
        honey_increase = (self.production_speed * time_elapsed)**0.9

        # Добавляем прирост меда к общему количеству
        self.collected_honey += honey_increase

        # Обновляем время последнего обновления
        self.last_update_time = current_time

    def collect_honey(self, count):
        self.update()
        collected_honey = min(count, self.collected_honey)
        self.collected_honey -= collected_honey
        return math.floor(collected_honey)

    def to_dict(self):
        building_dict = super().to_dict()
        return building_dict

    @classmethod
    def from_dict(cls, data):
        del data['production_speed']
        return cls(**data)


class StorageHive(Hive):
    def __init__(self, honey_storage=0, name='Медовый склад', level=1):
        super().__init__(name, level)
        self.honey_storage = honey_storage
        self.max_storage = self.level * 10  # максимальное количество мёда

    def __str__(self):
        attributes = [self.name + ':',  # название улья
                      'уровень: ' + str(self.level),  # уровень улья
                      'количество мёда: ' + str(math.floor(self.honey_storage)),  # количество собранного мёда
                      'максимальное количество мёда: ' + str(self.max_storage)
                      ]

        return '\n    '.join(attributes)

    def load(self, honey_count: HoneyBeehive):
        count = self.max_storage - self.honey_storage
        self.honey_storage += honey_count.collect_honey(count)

    def to_dict(self):
        building_dict = super().to_dict()
        return building_dict

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


if __name__ == "__main__":
    hive = HoneyBeehive(bee_count=111, level=1)
    hive2 = StorageHive()
    print(hive)

    zip_hive = hive.to_dict()
    time.sleep(1)

    unzip_hive = HoneyBeehive().from_dict(zip_hive)

    hive2.load(unzip_hive)
    print(hive2)
    print(unzip_hive)
