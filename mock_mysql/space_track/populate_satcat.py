# from mysql import get_cursor
# from mock_data.space_track.satcat import SATCAT_DATA

# def _main():
#     pass
#     # cursor = get_cursor()
#     # cursor.execute("""CREATE TABLE satcat (
#     #     INTLDES VARCHAR(20),
#     #     NORAD_CAT_ID VARCHAR(20) NOT NULL,
#     #     OBJECT_TYPE VARCHAR(20),
#     #     SATNAME VARCHAR(100),
#     #     COUNTRY VARCHAR(10),
#     #     LAUNCH VARCHAR(10),
#     #     SITE VARCHAR(10),
#     #     DECAY VARCHAR(10),
#     #     PERIOD VARCHAR(10),
#     #     INCLINATION VARCHAR(10),
#     #     APOGEE VARCHAR(10),
#     #     PERIGEE VARCHAR(10),
#     #     RCSVALUE VARCHAR(10),
#     #     RCS_SIZE VARCHAR(10),
#     #     FILE VARCHAR(15),
#     #     LAUNCH_YEAR VARCHAR(10),
#     #     LAUNCH_NUM VARCHAR(10),
#     #     LAUNCH_PIECE VARCHAR(10),
#     #     CURRENT VARCHAR(10),
#     #     OBJECT_NAME VARCHAR(50),
#     #     OBJECT_ID VARCHAR(20),
#     #     OBJECT_NUMBER VARCHAR(10),
#     #     PRIMARY KEY (NORAD_CAT_ID)
#     # )""")

#     # cursor.executemany("""INSERT INTO satcat (
#     #     INTLDES, NORAD_CAT_ID, OBJECT_TYPE, SATNAME, COUNTRY, LAUNCH,
#     #     SITE , DECAY , PERIOD , INCLINATION , APOGEE , PERIGEE , RCSVALUE ,
#     #     RCS_SIZE , FILE, LAUNCH_YEAR , LAUNCH_NUM , LAUNCH_PIECE ,
#     #     CURRENT , OBJECT_NAME, OBJECT_ID, OBJECT_NUMBER 
#     # ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", [
#     #     (v['INTLDES'], v['NORAD_CAT_ID'], v['OBJECT_TYPE'], v['SATNAME'], v['COUNTRY'], v['LAUNCH'], v['SITE'],
#     #      v['DECAY'], v['PERIOD'], v['INCLINATION'], v['APOGEE'], v['PERIGEE'], v['RCSVALUE'],
#     #      v['RCS_SIZE'], v['FILE'], v['LAUNCH_YEAR'], v['LAUNCH_NUM'], v['LAUNCH_PIECE'], v['CURRENT'],
#     #      v['OBJECT_NAME'], v['OBJECT_ID'], v['OBJECT_NUMBER'])
#     #     for v in SATCAT_DATA
#     # ])

# if __name__ == '__main__':
#     _main()