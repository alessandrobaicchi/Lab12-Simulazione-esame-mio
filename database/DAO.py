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

        # for row in cursor:
        #     # Faccio un controllo extra nel caso i cui avg_rating fosse NULL nel DB
        #     val = row["avg_rating"]
        #     if val is not None:
        #         results.append(float(val))      # Qui faccio la conversione da Decimal a float

        for row in cursor:
            results.append(row["avg_rating"])

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
                    select distinct n.id, n.name, n.date_of_birth  
                    from names n, role_mapping rm, movie m, ratings r  
                    where r.movie_id = m.id and m.id = rm.movie_id and rm.name_id = n.id 
                    and r.avg_rating BETWEEN %s AND %s              
                    AND n.date_of_birth IS NOT NULL
                """)
        # NOTA. BETWEEN INCLUDE gli estremi!

        cursor.execute(query, (startRange, endRange))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    # =================================================================================================



    # ===================================== Crea Grafo (Archi) ==============================================
    '''Attenzione. Il risultato è già filtrato! '''
    @staticmethod
    def getEdges(startRange, endRange):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("""
                 SELECT rm1.name_id AS actor1, rm2.name_id AS actor2, 
                    sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as Weight
                    FROM movie m, role_mapping rm1, role_mapping rm2, ratings r, 
                    names n1, names n2 
                    WHERE m.id = rm1.movie_id
                    and m.id = rm2.movie_id
                    and m.id = r.movie_id
                    and rm1.name_id = n1.id
                    and rm2.name_id = n2.id
                    and n1.date_of_birth IS NOT NULL
                    and n2.date_of_birth IS NOT null
                    and rm1.name_id < rm2.name_id
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and m.worlwide_gross_income is not null 
                    and m.worlwide_gross_income like '$%'
                    group by rm1.name_id, rm2.name_id

                 """)

        cursor.execute(query, (startRange, endRange))

        for row in cursor:
            results.append((row["actor1"], row["actor2"], row["Weight"]))
            # Potrei anche creare un DTO ad hoc...

        cursor.close()
        conn.close()

        return results

    # =================================================================================================
