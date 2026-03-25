import sqlite3
from scrapy.exceptions import DropItem


class BmwCleaningPipeline:
    def process_item(self, item, spider):
        if not item.get('model') or not item.get('name') or not item.get('registration'):
            raise DropItem(f"Missing required fields in: {item}")

        mileage = item.get('mileage')
        if mileage:
            mileage_clean = mileage.replace(',', '')
            if mileage_clean.isdigit():
                item['mileage'] = int(mileage_clean)
            else:
                item['mileage'] = None

        fuel = item.get('fuel')
        if fuel:
            item['fuel'] = fuel.lower()

        return item


class BmwSqlitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('bmw_cars.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                registration TEXT PRIMARY KEY,
                model TEXT,
                name TEXT,
                mileage INTEGER,
                registered TEXT,
                engine TEXT,
                range TEXT,
                exterior TEXT,
                fuel TEXT,
                transmission TEXT,
                upholstery TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT OR IGNORE INTO cars 
            (registration, model, name, mileage, registered, engine, range, exterior, fuel, transmission, upholstery) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('registration'),
            item.get('model'),
            item.get('name'),
            item.get('mileage'),
            item.get('registered'),
            item.get('engine'),
            item.get('range'),
            item.get('exterior'),
            item.get('fuel'),
            item.get('transmission'),
            item.get('upholstery')
        ))
        self.connection.commit()
        return item