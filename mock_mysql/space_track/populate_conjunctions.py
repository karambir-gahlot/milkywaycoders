# from mysql import get_cursor
# from mock_data.space_track.conjunctions import CONJUNCTIONS

# def _main():
#     pass
#     cursor = get_cursor()
#     cursor.execute("""CREATE TABLE conjunctions (
#         CDM_ID  VARCHAR(20) NOT NULL,
#         CREATED  VARCHAR(30),
#         EMERGENCY_REPORTABLE  VARCHAR(10),
#         TCA  VARCHAR(30),
#         MIN_RNG  VARCHAR(10),
#         PC   VARCHAR(20),
#         SAT_1_ID   VARCHAR(20),
#         SAT_1_NAME   VARCHAR(50),
#         SAT1_OBJECT_TYPE   VARCHAR(20),
#         SAT1_RCS   VARCHAR(20),
#         SAT_1_EXCL_VOL  VARCHAR(20),
#         SAT_2_ID   VARCHAR(20),
#         SAT_2_NAME   VARCHAR(50),
#         SAT2_OBJECT_TYPE  VARCHAR(20),
#         SAT2_RCS   VARCHAR(20),
#         SAT_2_EXCL_VOL   VARCHAR(20),
#         PRIMARY KEY(CDM_ID)
#     )""")

#     cursor.executemany("""INSERT INTO conjunctions (
#         CDM_ID, CREATED, EMERGENCY_REPORTABLE, TCA, MIN_RNG, PC,
#         SAT_1_ID , SAT_1_NAME , SAT1_OBJECT_TYPE , SAT1_RCS , SAT_1_EXCL_VOL , SAT_2_ID , SAT_2_NAME ,
#         SAT2_OBJECT_TYPE , SAT2_RCS, SAT_2_EXCL_VOL 
#     ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", [
#         (v['CDM_ID'], v['CREATED'], v['EMERGENCY_REPORTABLE'], v['TCA'], v['MIN_RNG'], v['PC'], v['SAT_1_ID'],
#          v['SAT_1_NAME'], v['SAT1_OBJECT_TYPE'], v['SAT1_RCS'], v['SAT_1_EXCL_VOL'], v['SAT_2_ID'], v['SAT_2_NAME'],
#          v['SAT2_OBJECT_TYPE'], v['SAT2_RCS'], v['SAT_2_EXCL_VOL'])
#         for v in CONJUNCTIONS
#     ])

# if __name__ == '__main__':
#     _main()