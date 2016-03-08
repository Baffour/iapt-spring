#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#


def RESET(db, cache):
    """
    Truncates the entire database and clears the cache.
    
    This will commit to the database, all database information
    WILL be lost!
    """
    cache.ram.clear()
    cache.disk.clear()
    for table in db.tables:
        db[table].truncate("CASCADE")
    db.commit()

class DBRowsFunctions():

    @classmethod
    def MAX(self, rows, column):
        max = None
        record = None
        for r in rows:
            if not max:
                max = r[column]
                record = r
            if r[column] > max:
                max = r[column]
                record = r

        return record, max

    @classmethod
    def MIN(self, rows, column):
        min = None
        record = None
        for r in rows:
            if not min:
                min = r[column]
                record = r
            if r[column] < min:
                min = r[column]
                record = r

        return record, min

    @classmethod
    def AVG(self, rows, column):
        avg = 0
        total = 0
        cnt = len(rows)
        for r in rows:
            total += r[column]
        avg = total / cnt
        return avg

    @classmethod
    def SUM(self, rows, column):
        total = 0
        for r in rows:
            total += r[column]
        return total
