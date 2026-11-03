from database.DB_connect import DBConnect
from model.circuit import Circuit


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT year
                    FROM seasons
                    ORDER BY year"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getAllNodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT distinct c.* 
                    FROM circuits c"""
        cursor.execute(query)
        # SELECT distinct c.*
        #                     FROM circuits c, races r
        #                     WHERE c.circuitId = r.circuitId


        res = []
        for row in cursor:
            res.append(Circuit(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdges(anno1, anno2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT t1.circuitId as uId, t2.circuitId as vId
FROM
                    (SELECT DISTINCT c.circuitId as circuitId 
                    FROM circuits c, races r
                    WHERE c.circuitId = r.circuitId
                    AND r.year > %s AND r.year < %s) t1, 
                    (SELECT DISTINCT c.circuitId as circuitId 
                    FROM circuits c, races r
                    WHERE c.circuitId = r.circuitId
                    AND r.year > %s AND r.year < %s) t2
 WHERE t1.circuitId < t2.circuitId"""
        cursor.execute(query, (anno1, anno2, anno1, anno2))

        res = []
        for row in cursor:
            res.append((row["uId"], row["vId"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getDiz(anno1, anno2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT c.circuitId as cirId, r.year as anno, re.driverId as driverId, re.time as tempo
FROM circuits c, races r, results re
WHERE c.circuitId = r.circuitId
AND r.raceId = re.raceId
AND r.year > %s AND r.year < %s;"""
        cursor.execute(query, (anno1, anno2))

        res = []
        for row in cursor:
            res.append((row["cirId"], row["anno"], row["driverId"], row["tempo"]))

        cursor.close()
        cnx.close()
        return res