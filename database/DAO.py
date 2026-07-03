from database.DB_connect import DBConnect
from model.actor import Actor


class DAO():
    def __init__(self):
        pass

    # =================================== DDs "Voto" ==============================================
    @staticmethod
    def getVoti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                    select distinct r.avg_rating 
                    from ratings r  
                    order by r.avg_rating asc
                     """)

        cursor.execute(query)

        for row in cursor:
            # Faccio un controllo extra nel caso i cui avg_rating fosse NULL nel DB
            val = row["avg_rating"]
            if val is not None:
                results.append(float(val))      # Qui faccio la conversione da Decimal a float

        cursor.close()
        conn.close()
        return results

    # =================================================================================================



    # ===================================== Crea Grafo (Nodi) ==============================================
    @staticmethod
    def getNodes(startRange, endRange):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                    select n.id, n.name, n.date_of_birth  
                    from names n, role_mapping rm, movie m, ratings r  
                    where r.movie_id = m.id and m.id = rm.movie_id and rm.name_id = n.id 
                    and r.avg_rating BETWEEN %s AND %s
                    AND rm.category IN ('actor', 'actress')
                    AND n.date_of_birth IS NOT NULL
                    AND YEAR(n.date_of_birth) >= 1900
                    AND YEAR(n.date_of_birth) <= YEAR(CURDATE())
                """)

        cursor.execute(query, (startRange, endRange))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    # =================================================================================================



    # ===================================== Crea Grafo (Archi) ==============================================
    '''Attenzione. Il risultato non è filtrato nè per il range dei voti
        e nè sul controllo delle date di nascita degli attori. I controlli si fanno nel Model.'''
    @staticmethod
    def getEdges(startRange, endRange):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                 SELECT rm1.name_id AS actor1, rm2.name_id AS actor2, m.worlwide_gross_income AS income
                 FROM role_mapping rm1
                          JOIN role_mapping rm2 ON rm1.movie_id = rm2.movie_id
                          JOIN movie m ON m.id = rm1.movie_id
                          JOIN ratings r ON r.movie_id = m.id
                 WHERE rm1.name_id < rm2.name_id
                   AND r.avg_rating BETWEEN %s AND %s
                   AND rm1.name_id IN (SELECT n.id
                                       FROM names n
                                                JOIN role_mapping rm ON rm.name_id = n.id
                                                JOIN movie m2 ON m2.id = rm.movie_id
                                                JOIN ratings r2 ON r2.movie_id = m2.id
                                       WHERE r2.avg_rating BETWEEN %s AND %s
                                                 AND rm.category IN ('actor', 'actress')
                                                 AND n.date_of_birth IS NOT NULL
                                                 AND YEAR (
                     n.date_of_birth) BETWEEN 1900
                   AND YEAR (CURDATE())
                     )
                   AND rm2.name_id IN (
                 SELECT n.id
                 FROM names n
                     JOIN role_mapping rm
                 ON rm.name_id = n.id
                     JOIN movie m2 ON m2.id = rm.movie_id
                     JOIN ratings r2 ON r2.movie_id = m2.id
                 WHERE r2.avg_rating BETWEEN %s
                   AND %s
                   AND rm.category IN ('actor'
                     , 'actress')
                   AND n.date_of_birth IS NOT NULL
                   AND YEAR (n.date_of_birth) BETWEEN 1900
                   AND YEAR (CURDATE())
                     )
                 """)

        cursor.execute(query, (
            startRange, endRange,
            startRange, endRange,
            startRange, endRange
        ))

        for row in cursor:
            results.append((row["actor1"], row["actor2"], row["income"]))
            # Potrei anche creare un DTO ad hoc...

        cursor.close()
        conn.close()

        return results

    # =================================================================================================
